"""
Conversation Memory — two-tier system
======================================
Tier 1 — Recent window  : last N raw messages (fast, always included)
Tier 2 — Summary layer  : older messages are compressed by Gemini into a
                           rolling summary that is prepended to the context.

Semantic search (pgvector) is implemented as an optional third tier:
when Supabase has the vector extension enabled and an embeddings table,
past turns matching the current query are surfaced even if they are
outside the recent window.

Schema additions needed (run once in Supabase SQL editor):
──────────────────────────────────────────────────────────
    -- 1. Enable pgvector
    create extension if not exists vector;

    -- 2. Summary table
    create table if not exists conversation_summaries (
        id          bigserial primary key,
        user_id     bigint    not null references users(id) on delete cascade,
        summary     text      not null,
        msg_count   int       not null default 0,
        created_at  timestamptz not null default now()
    );
    create index on conversation_summaries (user_id, created_at desc);

    -- 3. Message embeddings (optional — pgvector)
    create table if not exists message_embeddings (
        id          bigserial primary key,
        user_id     bigint    not null references users(id) on delete cascade,
        message_id  uuid      references messages(id) on delete cascade,
        role        text      not null,
        content     text      not null,
        embedding   vector(768),
        created_at  timestamptz not null default now()
    );
    create index on message_embeddings
        using ivfflat (embedding vector_cosine_ops) with (lists = 50);
──────────────────────────────────────────────────────────
"""
from __future__ import annotations

import logging
import threading
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)

# ── tuneable knobs ──────────────────────────────────────────────────────────

# How many recent raw messages to always keep verbatim in context
RECENT_WINDOW = 10

# After this many messages the oldest chunk is compressed into a summary
COMPRESS_THRESHOLD = 40

# How many semantically-similar past messages to inject (0 = disable)
SEMANTIC_TOP_K = 3


# ── lazy imports (avoid circular / missing-package errors at load time) ─────

def _get_supabase():
    from bot.db import _client  # noqa: PLC0415
    return _client


def _get_gemini_client():
    from bot.ai import client_manager  # noqa: PLC0415
    return client_manager.get()


# ── summary compression ─────────────────────────────────────────────────────

def _summarise_messages(messages: list[dict]) -> str:
    """Call Gemini to compress a list of messages into a concise summary."""
    from google.genai import types  # noqa: PLC0415

    if not messages:
        return ""

    transcript = "\n".join(
        f"{'User' if m['role'] == 'user' else 'Assistant'}: {m['content']}"
        for m in messages
    )

    prompt = (
        "Below is a chat transcript. Write a concise third-person summary "
        "(max 300 words) preserving key facts, decisions, and context. "
        "Do NOT include meta-commentary.\n\n" + transcript
    )

    try:
        client = _get_gemini_client()
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=[types.Content(role="user", parts=[types.Part(text=prompt)])],
            config=types.GenerateContentConfig(temperature=0.3, max_output_tokens=400),
        )
        return (response.text or "").strip()
    except Exception as exc:  # noqa: BLE001
        logger.warning("Summary generation failed: %s", exc)
        return ""


def get_or_create_summary(user_id: int) -> str:
    """
    Return the latest stored summary for a user (empty string if none).
    If the user has > COMPRESS_THRESHOLD messages and no fresh summary,
    trigger async compression in the background so the *next* request
    benefits from it (current request still works without blocking).
    """
    client = _get_supabase()

    try:
        row = (
            client.table("conversation_summaries")
            .select("summary, msg_count")
            .eq("user_id", user_id)
            .order("created_at", desc=True)
            .limit(1)
            .execute()
        )
        existing_summary = row.data[0]["summary"] if row.data else ""
        existing_count   = row.data[0]["msg_count"] if row.data else 0
    except Exception as exc:  # noqa: BLE001
        logger.warning("Failed to fetch summary for user %s: %s", user_id, exc)
        return ""

    # Count total messages
    try:
        total = (
            client.table("messages")
            .select("id", count="exact")
            .eq("user_id", user_id)
            .execute()
        )
        total_count = total.count or 0
    except Exception:  # noqa: BLE001
        total_count = 0

    # If we have enough new messages since last summary, compress in background
    new_since_summary = total_count - existing_count
    if new_since_summary >= COMPRESS_THRESHOLD:
        threading.Thread(
            target=_compress_and_store,
            args=(user_id, existing_count),
            daemon=True,
        ).start()

    return existing_summary


def _compress_and_store(user_id: int, already_summarised: int) -> None:
    """Fetch messages beyond the already-summarised point and store new summary."""
    client = _get_supabase()
    try:
        # Get messages older than the already-summarised window,
        # excluding the RECENT_WINDOW we always keep verbatim
        result = (
            client.table("messages")
            .select("role, content")
            .eq("user_id", user_id)
            .order("created_at", desc=False)
            .range(already_summarised, already_summarised + COMPRESS_THRESHOLD - 1)
            .execute()
        )
        messages = result.data or []
        if not messages:
            return

        new_summary = _summarise_messages(messages)
        if not new_summary:
            return

        client.table("conversation_summaries").insert({
            "user_id":   user_id,
            "summary":   new_summary,
            "msg_count": already_summarised + len(messages),
        }).execute()

        logger.info(
            "Compressed %d messages into summary for user %s",
            len(messages), user_id,
        )
    except Exception as exc:  # noqa: BLE001
        logger.warning("Compression failed for user %s: %s", user_id, exc)


# ── semantic search (pgvector, optional) ────────────────────────────────────

def _embed(text: str) -> list[float] | None:
    """Generate a text embedding via Gemini's embedding model."""
    try:
        client = _get_gemini_client()
        result = client.models.embed_content(
            model="text-embedding-004",
            contents=text,
        )
        return result.embeddings[0].values  # type: ignore[union-attr]
    except Exception as exc:  # noqa: BLE001
        logger.debug("Embed failed: %s", exc)
        return None


def semantic_search(user_id: int, query: str, top_k: int = SEMANTIC_TOP_K) -> list[dict]:
    """
    Return up to `top_k` past messages semantically similar to `query`.
    Returns [] silently if pgvector / embeddings table is unavailable.
    """
    if top_k <= 0:
        return []

    vec = _embed(query)
    if vec is None:
        return []

    client = _get_supabase()
    try:
        result = client.rpc(
            "match_message_embeddings",
            {
                "p_user_id":   user_id,
                "p_embedding": vec,
                "p_top_k":     top_k,
                "p_threshold": 0.75,
            },
        ).execute()
        return result.data or []
    except Exception as exc:  # noqa: BLE001
        logger.debug("Semantic search unavailable: %s", exc)
        return []


def store_embedding_async(user_id: int, message_id: str | None, role: str, content: str) -> None:
    """Fire-and-forget: embed a message and store in message_embeddings table."""
    threading.Thread(
        target=_store_embedding,
        args=(user_id, message_id, role, content),
        daemon=True,
    ).start()


def _store_embedding(user_id: int, message_id: str | None, role: str, content: str) -> None:
    vec = _embed(content)
    if vec is None:
        return
    client = _get_supabase()
    try:
        client.table("message_embeddings").insert({
            "user_id":    user_id,
            "message_id": message_id,
            "role":       role,
            "content":    content,
            "embedding":  vec,
        }).execute()
    except Exception as exc:  # noqa: BLE001
        logger.debug("Failed to store embedding: %s", exc)


# ── public helper used by handlers ──────────────────────────────────────────

def build_enriched_history(
    user_id: int,
    recent_messages: list[dict],
    current_query: str,
) -> list[dict]:
    """
    Combine:
      1. A summary of older messages (if any) as a synthetic "assistant" note
      2. Semantically-relevant past messages (if pgvector enabled)
      3. The recent raw window
    Returns a list in the same {role, content} format expected by ai.py.
    """
    enriched: list[dict] = []

    # 1. Summary layer
    summary = get_or_create_summary(user_id)
    if summary:
        enriched.append({
            "role":    "assistant",
            "content": f"[Earlier conversation summary]\n{summary}",
        })

    # 2. Semantic layer — past messages relevant to this query
    #    Skip entirely if conversation is still short: there's nothing
    #    outside the recent window worth searching, so don't pay for
    #    an extra embedding API call on every single message.
    if SEMANTIC_TOP_K > 0 and len(recent_messages) > RECENT_WINDOW:
        hits = semantic_search(user_id, current_query)
        if hits:
            # De-duplicate against recent window
            recent_contents = {m["content"] for m in recent_messages}
            unique_hits = [h for h in hits if h.get("content") not in recent_contents]
            if unique_hits:
                enriched.append({
                    "role":    "assistant",
                    "content": (
                        "[Relevant messages from earlier in our conversation]\n"
                        + "\n".join(
                            f"{'User' if h['role'] == 'user' else 'Assistant'}: {h['content']}"
                            for h in unique_hits
                        )
                    ),
                })

    # 3. Recent verbatim window
    enriched.extend(recent_messages[-RECENT_WINDOW:])

    return enriched
