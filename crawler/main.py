# ============================================================
# main.py — Crawler entry point + APScheduler
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

# ─── Fix Windows console encoding (cp1252 can't print box chars) ─
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# ─── Logging setup ───────────────────────────────────────────
log_file = os.path.join(os.path.dirname(__file__), "crawler.log")
file_handler = logging.handlers.RotatingFileHandler(
    log_file, maxBytes=10 * 1024 * 1024, backupCount=3, encoding="utf-8"
)
file_handler.setFormatter(logging.Formatter(
    "%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
))
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(logging.Formatter("%(levelname)-8s %(name)s  %(message)s"))

logging.basicConfig(level=logging.INFO, handlers=[file_handler, console_handler])
logger = logging.getLogger(__name__)

# ─── Import after env + logging are configured ───────────────
from fetcher import fetch_and_deduplicate
from processor import process_articles, generate_trending_topics
from database import (
    get_existing_urls,
    save_articles,
    recalculate_category_counts,
    save_trending_topics,
    get_recent_titles,
)


# ─────────────────────────────────────────────────────────────
# Crawl cycle (every 5 minutes)
# ─────────────────────────────────────────────────────────────

async def crawl_cycle() -> None:
    logger.info("=== Crawl cycle started ===")
    try:
        articles = await fetch_and_deduplicate()
        if not articles:
            logger.info("No articles fetched this cycle")
            return

        existing_urls = get_existing_urls()
        new_articles = [a for a in articles if a["source_url"] not in existing_urls]
        logger.info(
            "New articles to process: %d (skipping %d existing)",
            len(new_articles), len(articles) - len(new_articles),
        )
        if not new_articles:
            return

        enriched = await process_articles(new_articles)
        save_articles(enriched)

    except Exception as exc:
        logger.exception("Crawl cycle failed: %s", exc)
    finally:
        logger.info("=== Crawl cycle complete ===")


# ─────────────────────────────────────────────────────────────
# Hourly tasks
# ─────────────────────────────────────────────────────────────

async def hourly_tasks() -> None:
    logger.info("--- Hourly tasks started ---")
    try:
        titles = get_recent_titles(50)
        if titles:
            topics = generate_trending_topics(titles)
            save_trending_topics(topics)
        recalculate_category_counts()
    except Exception as exc:
        logger.exception("Hourly tasks failed: %s", exc)
    finally:
        logger.info("--- Hourly tasks complete ---")


# ─────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────

async def main() -> None:
    logger.info("NewsAI Crawler starting up...")

    await crawl_cycle()
    await hourly_tasks()

    scheduler = AsyncIOScheduler()
    scheduler.add_job(crawl_cycle,  "interval", minutes=5, id="crawl")
    scheduler.add_job(hourly_tasks, "interval", hours=1,   id="hourly")
    scheduler.start()

    logger.info("Scheduler running. Crawl every 5 min, hourly tasks every 1 hr.")

    try:
        while True:
            await asyncio.sleep(60)
    except (KeyboardInterrupt, SystemExit):
        logger.info("Shutting down...")
        scheduler.shutdown()


if __name__ == "__main__":
    asyncio.run(main())