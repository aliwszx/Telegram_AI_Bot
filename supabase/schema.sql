-- ============================================================
-- Telegram AI Bot — Supabase schema
-- Run this in: Supabase Dashboard → SQL Editor → New query → Run
-- ============================================================

-- Needed for gen_random_uuid()
create extension if not exists "pgcrypto";

-- ---------------------------------------------------------------
-- users: one row per Telegram user. id = Telegram user_id (bigint)
-- ---------------------------------------------------------------
create table if not exists users (
    id              bigint primary key,            -- Telegram user_id
    username        text,
    first_name      text,
    plan            text not null default 'free'   -- 'free' | 'premium'
                        check (plan in ('free', 'premium')),
    daily_usage     integer not null default 0,     -- messages sent today
    last_usage_date date not null default current_date,
    created_at      timestamptz not null default now()
);

-- ---------------------------------------------------------------
-- messages: chat history, used to give Gemini conversational context
-- ---------------------------------------------------------------
create table if not exists messages (
    id         uuid primary key default gen_random_uuid(),
    user_id    bigint not null references users(id) on delete cascade,
    role       text not null check (role in ('user', 'assistant')),
    content    text not null,
    created_at timestamptz not null default now()
);

-- Speeds up "last 10 messages per user" lookups
create index if not exists idx_messages_user_created
    on messages (user_id, created_at desc);

-- ---------------------------------------------------------------
-- Row Level Security
-- The bot talks to Supabase using the SERVICE ROLE key, which bypasses RLS,
-- so this is mainly a safety net in case the anon/public key is ever used
-- from a client app later (e.g. an admin dashboard).
-- ---------------------------------------------------------------
alter table users enable row level security;
alter table messages enable row level security;

-- No public policies are created on purpose: only the service_role key
-- (used by the bot backend) can read/write. Add policies here later if you
-- build a user-facing dashboard with Supabase Auth.
