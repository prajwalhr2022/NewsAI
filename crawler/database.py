# ============================================================
# database.py — Supabase read / write for the crawler
# ============================================================

import logging
import os
from typing import Any

from supabase import create_client, Client

logger = logging.getLogger(__name__)

_client: Client | None = None


def get_client() -> Client:
    global _client
    if _client is None:
        _client = create_client(
            os.environ["SUPABASE_URL"],
            os.environ["SUPABASE_SERVICE_ROLE_KEY"],
        )
    return _client


def get_existing_urls(limit: int = 2000) -> set[str]:
    """Return URLs already saved so we skip re-processing them."""
    client = get_client()
    try:
        resp = (
            client.table("articles")
            .select("source_url")
            .order("fetched_at", desc=True)
            .limit(limit)
            .execute()
        )
        return {row["source_url"] for row in (resp.data or [])}
    except Exception as exc:
        logger.error("Failed to fetch existing URLs: %s", exc)
        return set()


def save_articles(articles: list[dict[str, Any]]) -> int:
    """Upsert articles. Returns number saved."""
    if not articles:
        return 0

    client = get_client()
    saved = 0
    ALLOWED = {
        "title", "summary", "source_url", "source_name", "image_url",
        "category", "subcategory", "is_india_focused", "language",
        "trend_score", "verification_status", "source_count",
        "published_at", "tags", "related_sources", "translations",
    }
    CHUNK = 20

    for i in range(0, len(articles), CHUNK):
        rows = [{k: v for k, v in a.items() if k in ALLOWED}
                for a in articles[i : i + CHUNK]]
        try:
            client.table("articles").upsert(rows, on_conflict="source_url").execute()
            saved += len(rows)
        except Exception as exc:
            logger.error("Upsert chunk failed: %s", exc)

    logger.info("Saved %d/%d articles to Supabase", saved, len(articles))
    return saved


def recalculate_category_counts() -> None:
    """
    Recalculate article_count per category and subcategory.
    Uses upsert on slug (unique) so duplicate name errors never happen.
    """
    client = get_client()
    try:
        resp = client.table("articles").select("category, subcategory").execute()
        rows = resp.data or []

        cat_counts: dict[str, int] = {}
        subcat_counts: dict[tuple[str, str], int] = {}

        for row in rows:
            cat = row.get("category")
            sub = row.get("subcategory")
            if cat:
                cat_counts[cat] = cat_counts.get(cat, 0) + 1
            if cat and sub:
                subcat_counts[(cat, sub)] = subcat_counts.get((cat, sub), 0) + 1

        def to_slug(name: str) -> str:
            return name.lower().replace(" & ", "-").replace(" ", "-")

        # Upsert top-level categories — conflict on slug only (slug is unique)
        for cat_name, count in cat_counts.items():
            slug = to_slug(cat_name)
            client.table("categories").upsert(
                {"name": cat_name, "slug": slug, "parent_slug": None, "article_count": count},
                on_conflict="slug",
            ).execute()

        # Upsert subcategories
        for (cat_name, sub_name), count in subcat_counts.items():
            if not sub_name:
                continue
            parent_slug = to_slug(cat_name)
            sub_slug = f"{parent_slug}-{sub_name.lower().replace(' ', '-')}"
            client.table("categories").upsert(
                {"name": sub_name, "slug": sub_slug, "parent_slug": parent_slug, "article_count": count},
                on_conflict="slug",
            ).execute()

        logger.info(
            "Category counts updated — %d categories, %d subcategories",
            len(cat_counts), len(subcat_counts),
        )
    except Exception as exc:
        logger.error("Category recalculation failed: %s", exc)


def save_trending_topics(topics: list[dict[str, Any]]) -> None:
    """Replace all trending topics with the fresh list."""
    client = get_client()
    try:
        client.table("trending_topics").delete().neq(
            "id", "00000000-0000-0000-0000-000000000000"
        ).execute()
        if topics:
            client.table("trending_topics").insert(topics).execute()
        logger.info("Saved %d trending topics", len(topics))
    except Exception as exc:
        logger.error("Trending topics save failed: %s", exc)


def get_recent_titles(limit: int = 50) -> list[str]:
    client = get_client()
    try:
        resp = (
            client.table("articles")
            .select("title")
            .order("fetched_at", desc=True)
            .limit(limit)
            .execute()
        )
        return [row["title"] for row in (resp.data or [])]
    except Exception as exc:
        logger.error("Failed to fetch recent titles: %s", exc)
        return []