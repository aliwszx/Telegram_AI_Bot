-- ============================================================
-- Telegram AI Bot — Supabase schema (v2)
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
    chat_mode       text not null default 'default',   -- NEW: AI persona
    created_at      timestamptz not null default now()
);

-- Add chat_mode to existing deployments (safe to run on existing DB)
alter table users add column if not exists chat_mode text not null default 'default';
alter table users add column if not exists premium_until timestamptz;

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
-- Row Level Security
-- ---------------------------------------------------------------
alter table users enable row level security;
alter table messages enable row level security;
