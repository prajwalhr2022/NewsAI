# ============================================================
# main.py — NewsAI News Crawler
# Crawls every 20 minutes
# ============================================================

import asyncio
import io
import logging
import logging.handlers
import os
import sys

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv

load_dotenv()

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

log_file = os.path.join(os.path.dirname(__file__), "crawler.log")
file_handler = logging.handlers.RotatingFileHandler(
    log_file, maxBytes=10 * 1024 * 1024, backupCount=3, encoding="utf-8"
)
file_handler.setFormatter(logging.Formatter(
    "%(asctime)s  %(levelname)-8s  %(name)s  %(message)s", datefmt="%Y-%m-%d %H:%M:%S",
))
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(logging.Formatter("%(levelname)-8s %(name)s  %(message)s"))
logging.basicConfig(level=logging.INFO, handlers=[file_handler, console_handler])
logger = logging.getLogger(__name__)

from fetcher import fetch_and_deduplicate
from processor import process_articles, generate_trending_topics
from database import (
    get_existing_urls, save_articles,
    recalculate_category_counts, save_trending_topics, get_recent_titles,
)

# 20 min cycle × 72 cycles/day × 100 articles = 7200 AI calls/day
# Groq: 100k tokens/day → ~70 articles with summaries safely
# Gemini: 1500 req/day → 1500 categorisation calls safely
MAX_AI_ARTICLES_PER_RUN = 100


async def crawl_cycle() -> None:
    logger.info("=== Crawl cycle started ===")
    try:
        articles = await fetch_and_deduplicate()
        if not articles:
            logger.info("No articles fetched")
            return

        existing_urls = get_existing_urls()
        new_articles = [a for a in articles if a["source_url"] not in existing_urls]
        logger.info("New: %d  Existing: %d", len(new_articles), len(articles) - len(new_articles))

        if not new_articles:
            return

        ai_batch       = new_articles[:MAX_AI_ARTICLES_PER_RUN]
        fallback_batch = new_articles[MAX_AI_ARTICLES_PER_RUN:]

        enriched = await process_articles(ai_batch)

        for a in fallback_batch:
            enriched.append({
                "title":               a["title"],
                "summary":             (a.get("description") or a.get("title") or "")[:200],
                "source_url":          a["source_url"],
                "source_name":         a["source_name"],
                "image_url":           a.get("image_url"),
                "category":            a.get("category", "World Affairs"),
                "subcategory":         None,
                "is_india_focused":    a.get("region") == "india",
                "language":            "en",
                "trend_score":         10,
                "verification_status": "unverified",
                "source_count":        a.get("source_count", 1),
                "published_at":        a.get("published_at"),
                "tags":                [],
                "related_sources":     a.get("related_sources", []),
                "translations":        {},
            })

        save_articles(enriched)

    except Exception as exc:
        logger.exception("Crawl cycle failed: %s", exc)
    finally:
        logger.info("=== Crawl cycle complete ===")


async def trending_tasks() -> None:
    logger.info("--- Trending refresh ---")
    try:
        titles = get_recent_titles(50)
        if titles:
            save_trending_topics(generate_trending_topics(titles))
        recalculate_category_counts()
    except Exception as exc:
        logger.exception("Trending tasks failed: %s", exc)


async def main() -> None:
    logger.info("NewsAI Crawler starting — 20 min crawl cycle")
    await crawl_cycle()
    await trending_tasks()

    scheduler = AsyncIOScheduler()
    # Crawl every 20 minutes
    scheduler.add_job(crawl_cycle,    "interval", minutes=20, id="crawl")
    # Refresh trending every 20 minutes too
    scheduler.add_job(trending_tasks, "interval", minutes=20, id="trending")
    scheduler.start()

    logger.info("Scheduler running. Crawl + trending every 20 min.")
    try:
        while True:
            await asyncio.sleep(60)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
