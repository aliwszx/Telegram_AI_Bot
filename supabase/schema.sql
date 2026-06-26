-- ============================================================
--  Telegram AI Bot PRO — Supabase Schema
--  Run this in the Supabase SQL Editor (Dashboard → SQL Editor)
-- ============================================================

-- ── Extensions ───────────────────────────────────────────────
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";  -- for fast username search

-- ── Users table ───────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS users (
    id                BIGINT PRIMARY KEY,          -- Telegram user_id
    username          TEXT,
    first_name        TEXT,
    language_code     TEXT,
    preferred_lang    TEXT,                       -- user-chosen UI language (az/en/ru)

    plan              TEXT    NOT NULL DEFAULT 'free'
                      CHECK (plan IN ('free', 'premium')),
    premium_until     TIMESTAMPTZ,

    daily_usage       INTEGER NOT NULL DEFAULT 0,
    last_usage_date   DATE    NOT NULL DEFAULT CURRENT_DATE,
    bonus_messages    INTEGER NOT NULL DEFAULT 0,

    chat_mode         TEXT    NOT NULL DEFAULT 'default',
    web_search        BOOLEAN NOT NULL DEFAULT TRUE,

    referred_by       BIGINT  REFERENCES users(id),
    referral_count    INTEGER NOT NULL DEFAULT 0,

    total_payments    INTEGER NOT NULL DEFAULT 0,
    total_stars_spent INTEGER NOT NULL DEFAULT 0,

    created_at        TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at        TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_users_username   ON users USING gin (username gin_trgm_ops);
CREATE INDEX IF NOT EXISTS idx_users_plan        ON users (plan);
CREATE INDEX IF NOT EXISTS idx_users_last_usage  ON users (last_usage_date);
CREATE INDEX IF NOT EXISTS idx_users_premium_until ON users (premium_until)
    WHERE plan = 'premium';

-- Auto-update updated_at
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_users_updated_at
BEFORE UPDATE ON users
FOR EACH ROW EXECUTE FUNCTION update_updated_at();


-- ── Messages table ────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS messages (
    id         BIGSERIAL PRIMARY KEY,
    user_id    BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role       TEXT   NOT NULL CHECK (role IN ('user', 'assistant')),
    content    TEXT   NOT NULL,
    topic      TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_messages_user_created
    ON messages (user_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_messages_topic
    ON messages (topic) WHERE topic IS NOT NULL;


-- ── Payments table ────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS payments (
    id         BIGSERIAL PRIMARY KEY,
    user_id    BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    stars      INTEGER NOT NULL DEFAULT 0,
    days       INTEGER NOT NULL DEFAULT 30,
    plan       TEXT    NOT NULL DEFAULT 'premium',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_payments_user    ON payments (user_id);
CREATE INDEX IF NOT EXISTS idx_payments_created ON payments (created_at DESC);


-- ── Feedback table ────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS feedback (
    id         BIGSERIAL PRIMARY KEY,
    user_id    BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    text       TEXT   NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);


-- ── RPC: check_usage_and_get_history ─────────────────────────
--  Hot path: single round-trip per AI message
CREATE OR REPLACE FUNCTION check_usage_and_get_history(
    p_user_id    BIGINT,
    p_free_limit INTEGER DEFAULT 20,
    p_prem_limit INTEGER DEFAULT 500,
    p_hist_limit INTEGER DEFAULT 15
)
RETURNS JSONB
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
    v_user        users%ROWTYPE;
    v_today       DATE := CURRENT_DATE;
    v_usage       INTEGER;
    v_limit       INTEGER;
    v_allowed     BOOLEAN;
    v_history     JSONB;
    v_plan        TEXT;
BEGIN
    SELECT * INTO v_user FROM users WHERE id = p_user_id;
    IF NOT FOUND THEN
        RAISE EXCEPTION 'User % not found', p_user_id;
    END IF;

    -- Determine effective plan (expire check)
    v_plan := v_user.plan;
    IF v_plan = 'premium' AND v_user.premium_until IS NOT NULL
       AND v_user.premium_until < NOW() THEN
        UPDATE users SET plan = 'free', premium_until = NULL WHERE id = p_user_id;
        v_plan := 'free';
    END IF;

    -- Reset daily usage if date changed
    v_usage := v_user.daily_usage;
    IF v_user.last_usage_date IS DISTINCT FROM v_today THEN
        v_usage := 0;
    END IF;

    -- Compute limit (plan + bonus)
    v_limit := CASE WHEN v_plan = 'premium' THEN p_prem_limit ELSE p_free_limit END
               + COALESCE(v_user.bonus_messages, 0);

    -- Check and increment
    IF v_usage >= v_limit THEN
        v_allowed := FALSE;
        UPDATE users SET daily_usage = v_usage, last_usage_date = v_today WHERE id = p_user_id;
    ELSE
        v_allowed := TRUE;
        v_usage   := v_usage + 1;
        UPDATE users SET daily_usage = v_usage, last_usage_date = v_today WHERE id = p_user_id;
    END IF;

    -- Fetch recent history
    SELECT COALESCE(jsonb_agg(row_to_json(m.*) ORDER BY m.created_at ASC), '[]'::jsonb)
    INTO v_history
    FROM (
        SELECT role, content, created_at
        FROM messages
        WHERE user_id = p_user_id
        ORDER BY created_at DESC
        LIMIT p_hist_limit
    ) m;

    RETURN jsonb_build_object(
        'allowed',    v_allowed,
        'usage',      v_usage,
        'limit',      v_limit,
        'plan',       v_plan,
        'chat_mode',  COALESCE(v_user.chat_mode, 'default'),
        'web_search', COALESCE(v_user.web_search, TRUE),
        'history',    v_history
    );
END;
$$;


-- ── Row Level Security ────────────────────────────────────────
ALTER TABLE users    ENABLE ROW LEVEL SECURITY;
ALTER TABLE messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE payments ENABLE ROW LEVEL SECURITY;
ALTER TABLE feedback ENABLE ROW LEVEL SECURITY;

-- Service role (used by bot) bypasses RLS automatically.
-- No extra policies needed for the bot's service key.

-- ── Useful views for Supabase dashboard ──────────────────────
CREATE OR REPLACE VIEW daily_summary AS
SELECT
    last_usage_date                            AS date,
    COUNT(*)                                   AS active_users,
    SUM(daily_usage)                           AS total_messages,
    COUNT(*) FILTER (WHERE plan = 'premium')   AS premium_active
FROM users
GROUP BY last_usage_date
ORDER BY last_usage_date DESC;

CREATE OR REPLACE VIEW revenue_summary AS
SELECT
    DATE_TRUNC('month', created_at) AS month,
    COUNT(*)                         AS payments,
    SUM(stars)                       AS total_stars
FROM payments
GROUP BY month
ORDER BY month DESC;


-- ── Migration: add preferred_lang column (run once if upgrading) ──────────
-- ALTER TABLE users ADD COLUMN IF NOT EXISTS preferred_lang TEXT;


-- ── Atomic counter helpers ────────────────────────────────────────────────
-- Avoids read-modify-write races when incrementing bonus_messages or
-- payment counters from application code.

CREATE OR REPLACE FUNCTION increment_bonus_messages(p_user_id bigint, p_amount int)
RETURNS void LANGUAGE sql AS $$
  UPDATE users
  SET bonus_messages = COALESCE(bonus_messages, 0) + p_amount
  WHERE id = p_user_id;
$$;

CREATE OR REPLACE FUNCTION increment_payment_counters(p_user_id bigint, p_stars int)
RETURNS void LANGUAGE sql AS $$
  UPDATE users
  SET total_payments    = COALESCE(total_payments, 0) + 1,
      total_stars_spent = COALESCE(total_stars_spent, 0) + p_stars
  WHERE id = p_user_id;
$$;
