-- ============================================================
-- Telegram AI Bot — Supabase schema (v3)
-- Run this in: Supabase Dashboard → SQL Editor → New query → Run
-- ============================================================

create extension if not exists "pgcrypto";

-- ---------------------------------------------------------------
-- users
-- ---------------------------------------------------------------
create table if not exists users (
    id              bigint primary key,
    username        text,
    first_name      text,
    plan            text not null default 'free'
                        check (plan in ('free', 'premium')),
    daily_usage     integer not null default 0,
    last_usage_date date not null default current_date,
    premium_until   timestamptz,
    chat_mode       text not null default 'default',
    created_at      timestamptz not null default now()
);

alter table users add column if not exists chat_mode       text not null default 'default';
alter table users add column if not exists premium_until   timestamptz;
alter table users add column if not exists bonus_messages  integer not null default 0;
alter table users add column if not exists referred_by     bigint;
alter table users add column if not exists referral_count  integer not null default 0;
alter table users add column if not exists web_search      boolean not null default true;

-- ---------------------------------------------------------------
-- messages
-- ---------------------------------------------------------------
create table if not exists messages (
    id         uuid primary key default gen_random_uuid(),
    user_id    bigint not null references users(id) on delete cascade,
    role       text not null check (role in ('user', 'assistant')),
    content    text not null,
    created_at timestamptz not null default now()
);

create index if not exists idx_messages_user_created
    on messages (user_id, created_at desc);

-- ---------------------------------------------------------------
-- RPC: check_usage_and_get_history
-- Single call instead of 3 separate queries per message
-- ---------------------------------------------------------------
create or replace function check_usage_and_get_history(
    p_user_id    bigint,
    p_free_limit  integer,
    p_prem_limit  integer,
    p_hist_limit  integer
)
returns json
language plpgsql
as $$
declare
    v_user       users%rowtype;
    v_plan       text;
    v_limit      integer;
    v_today      date := current_date;
    v_usage      integer;
    v_allowed    boolean;
    v_history    json;
begin
    -- Lock row for update to prevent race conditions
    select * into v_user from users where id = p_user_id for update;

    if not found then
        raise exception 'user_not_found';
    end if;

    -- Check premium expiry
    v_plan := v_user.plan;
    if v_plan = 'premium' and v_user.premium_until is not null
       and v_user.premium_until < now() then
        v_plan := 'free';
        update users set plan = 'free', premium_until = null where id = p_user_id;
    end if;

    v_limit := case when v_plan = 'premium' then p_prem_limit else p_free_limit end
               + coalesce(v_user.bonus_messages, 0);

    -- Reset daily counter if needed
    v_usage := case when v_user.last_usage_date = v_today then v_user.daily_usage else 0 end;

    if v_usage >= v_limit then
        v_allowed := false;
    else
        v_allowed := true;
        v_usage := v_usage + 1;
        update users
           set daily_usage     = v_usage,
               last_usage_date = v_today
         where id = p_user_id;
    end if;

    -- Fetch recent history
    select json_agg(m order by m.created_at asc)
      into v_history
      from (
          select role, content, created_at
            from messages
           where user_id = p_user_id
           order by created_at desc
           limit p_hist_limit
      ) m;

    return json_build_object(
        'allowed',   v_allowed,
        'usage',     v_usage,
        'limit',     v_limit,
        'plan',      v_plan,
        'chat_mode', v_user.chat_mode,
        'history',   coalesce(v_history, '[]'::json)
    );
end;
$$;

-- ---------------------------------------------------------------
-- Row Level Security
-- ---------------------------------------------------------------
alter table users    enable row level security;
alter table messages enable row level security;
