# ============================================================
# fetcher.py — Async RSS fetcher + two-pass deduplication
# ============================================================

import asyncio
import hashlib
import logging
import re
import string
from datetime import datetime, timezone
from typing import Any

import feedparser
import httpx

from sources import SOURCES, SOURCE_NAME_TO_TIER

logger = logging.getLogger(__name__)

# ─── Stopwords for Jaccard title normalisation ───────────────
STOPWORDS = {
    "a", "an", "the", "and", "or", "but", "in", "on", "at", "to",
    "for", "of", "with", "by", "from", "up", "about", "into", "over",
    "is", "are", "was", "were", "be", "been", "being", "has", "have",
    "had", "do", "does", "did", "will", "would", "could", "should",
    "may", "might", "shall", "can", "this", "that", "it", "its",
    "he", "she", "they", "we", "you", "i", "as", "after", "before",
    "says", "said", "new", "not", "no",
}

BATCH_SIZE = 20          # concurrent feed fetches
JACCARD_THRESHOLD = 0.55  # minimum similarity to merge stories


# ─────────────────────────────────────────────────────────────
# Title normalisation helpers
# ─────────────────────────────────────────────────────────────

def _normalise_title(title: str) -> frozenset[str]:
    """Lowercase, strip punctuation, remove stopwords, return word set."""
    title = title.lower()
    title = title.translate(str.maketrans("", "", string.punctuation))
    words = title.split()
    return frozenset(w for w in words if w not in STOPWORDS and len(w) > 1)


def _jaccard(set_a: frozenset, set_b: frozenset) -> float:
    if not set_a or not set_b:
        return 0.0
    intersection = len(set_a & set_b)
    union = len(set_a | set_b)
    return intersection / union if union else 0.0


def _url_key(url: str) -> str:
    """Stable SHA-256 key for a URL (strips tracking params crudely)."""
    clean = url.split("?")[0].rstrip("/").lower()
    return hashlib.sha256(clean.encode()).hexdigest()


# ─────────────────────────────────────────────────────────────
# Fetch a single RSS feed
# ─────────────────────────────────────────────────────────────

async def _fetch_feed(
    client: httpx.AsyncClient,
    source: dict[str, Any],
) -> list[dict[str, Any]]:
    """Fetch one RSS feed and return a list of raw article dicts."""
    articles: list[dict[str, Any]] = []
    try:
        resp = await client.get(source["url"], timeout=15)
        resp.raise_for_status()
        feed = feedparser.parse(resp.text)

        for entry in feed.entries[:30]:  # cap at 30 per feed
            title = getattr(entry, "title", "").strip()
            if not title:
                continue

            link = getattr(entry, "link", "").strip()
            if not link:
                continue

            # Parse published date
            pub_date: datetime | None = None
            if hasattr(entry, "published_parsed") and entry.published_parsed:
                try:
                    pub_date = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
                except Exception:
                    pass

            # Extract image from media or enclosures
            image_url: str | None = None
            if hasattr(entry, "media_content") and entry.media_content:
                image_url = entry.media_content[0].get("url")
            elif hasattr(entry, "enclosures") and entry.enclosures:
                enc = entry.enclosures[0]
                if enc.get("type", "").startswith("image"):
                    image_url = enc.get("href") or enc.get("url")

            description = ""
            if hasattr(entry, "summary"):
                # Strip basic HTML tags from summary
                description = re.sub(r"<[^>]+>", "", entry.summary).strip()[:500]

            articles.append({
                "title":        title,
                "source_url":   link,
                "source_name":  source["name"],
                "tier":         source["tier"],
                "region":       source["region"],
                "category":     source["category"],
                "description":  description,
                "image_url":    image_url,
                "published_at": pub_date.isoformat() if pub_date else None,
                "_url_key":     _url_key(link),
                "_title_set":   _normalise_title(title),
            })

    except Exception as exc:
        logger.warning("Feed failed [%s]: %s", source["name"], exc)

    return articles


# ─────────────────────────────────────────────────────────────
# Fetch all feeds in batches of BATCH_SIZE
# ─────────────────────────────────────────────────────────────

async def fetch_all_feeds() -> list[dict[str, Any]]:
    """Fetch all RSS sources concurrently in batches. Returns raw articles."""
    all_articles: list[dict[str, Any]] = []

    limits = httpx.Limits(max_connections=BATCH_SIZE, max_keepalive_connections=10)
    headers = {"User-Agent": "NewsAI-Crawler/1.0 (+https://github.com/newsai)"}

    async with httpx.AsyncClient(limits=limits, headers=headers, follow_redirects=True) as client:
        for i in range(0, len(SOURCES), BATCH_SIZE):
            batch = SOURCES[i : i + BATCH_SIZE]
            tasks = [_fetch_feed(client, source) for source in batch]
            results = await asyncio.gather(*tasks, return_exceptions=False)
            for result in results:
                all_articles.extend(result)
            logger.info("Batch %d/%d fetched — %d articles so far",
                        i // BATCH_SIZE + 1,
                        -(-len(SOURCES) // BATCH_SIZE),
                        len(all_articles))

    logger.info("Total raw articles fetched: %d", len(all_articles))
    return all_articles


# ─────────────────────────────────────────────────────────────
# Pass 1 — URL deduplication
# ─────────────────────────────────────────────────────────────

def deduplicate_by_url(articles: list[dict]) -> list[dict]:
    """Remove exact duplicate URLs. Keep first occurrence."""
    seen: set[str] = set()
    unique: list[dict] = []
    for article in articles:
        key = article["_url_key"]
        if key not in seen:
            seen.add(key)
            unique.append(article)
    logger.info("After URL dedup: %d articles (removed %d)",
                len(unique), len(articles) - len(unique))
    return unique


# ─────────────────────────────────────────────────────────────
# Pass 2 — Cross-source story merging (Jaccard similarity)
# ─────────────────────────────────────────────────────────────

def merge_duplicate_stories(articles: list[dict]) -> list[dict]:
    """
    Merge articles covering the same story.
    - Sort so Tier 1 sources come first (become the base article)
    - Compare Jaccard similarity on normalised title word sets
    - If ≥ JACCARD_THRESHOLD: merge into the base article
    """
    # Sort: tier 1 first so they become the base
    articles = sorted(articles, key=lambda a: (a["tier"], a.get("published_at") or ""))

    merged: list[dict] = []
    skip_indices: set[int] = set()

    for i, base in enumerate(articles):
        if i in skip_indices:
            continue

        related: list[dict] = []
        base_set = base["_title_set"]

        for j in range(i + 1, len(articles)):
            if j in skip_indices:
                continue
            candidate = articles[j]
            sim = _jaccard(base_set, candidate["_title_set"])
            if sim >= JACCARD_THRESHOLD:
                related.append(candidate)
                skip_indices.add(j)

        source_count = 1 + len(related)
        trend_boost = min(30, (source_count - 1) * 10)

        # Build related_sources list
        related_sources = [
            {"name": r["source_name"], "url": r["source_url"], "tier": r["tier"]}
            for r in related
        ]

        # Auto-upgrade verification status
        has_tier1_base = base["tier"] == 1
        has_tier1_related = any(r["tier"] == 1 for r in related)
        if source_count >= 3 or (has_tier1_base and source_count >= 2) or (has_tier1_related and source_count >= 2):
            verification_status = "confirmed"
        else:
            verification_status = "unverified"

        merged_article = {
            **base,
            "source_count":        source_count,
            "trend_boost":         trend_boost,
            "related_sources":     related_sources,
            "verification_status": verification_status,
        }
        # Remove internal-only keys before returning
        merged_article.pop("_url_key", None)
        merged_article.pop("_title_set", None)
        merged_article.pop("tier", None)

        merged.append(merged_article)

    logger.info("After story merge: %d unique stories (merged from %d articles)",
                len(merged), len(articles))
    return merged


# ─────────────────────────────────────────────────────────────
# Public entry point
# ─────────────────────────────────────────────────────────────

async def fetch_and_deduplicate() -> list[dict]:
    """Full pipeline: fetch → URL dedup → story merge."""
    raw = await fetch_all_feeds()
    after_url_dedup = deduplicate_by_url(raw)
    final = merge_duplicate_stories(after_url_dedup)
    return final