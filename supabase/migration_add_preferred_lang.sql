-- Run this once in Supabase SQL Editor if you already have an existing database
ALTER TABLE users ADD COLUMN IF NOT EXISTS preferred_lang TEXT;
