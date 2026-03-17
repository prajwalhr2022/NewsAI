# ============================================================
# processor.py — AI processing via Groq (summarise) + Gemini (categorise)
# Uses: google-genai (new SDK), groq
# ============================================================

import asyncio
import json
import logging
import os
import re
from typing import Any

from google import genai
from google.genai import types
from groq import Groq

logger = logging.getLogger(__name__)

# ─── Groq client ─────────────────────────────────────────────
groq_client = Groq(api_key=os.environ["GROQ_API_KEY"])

# ─── Gemini client (new SDK) ─────────────────────────────────
gemini_client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
GEMINI_MODEL = "gemini-2.0-flash"   # free tier: 1500 req/day, 1M tokens/min

BATCH_SIZE = 5
MAX_AI_BATCHES_PER_RUN = 40 

VALID_CATEGORIES = {
    "Politics", "Technology", "Business & Economy", "Sports",
    "Science & Space", "Health & Medicine", "Entertainment",
    "Environment & Climate", "World Affairs", "Crime & Law",
    "Education", "Lifestyle", "Defence & Security",
}


def _extract_json(text: str) -> Any:
    text = re.sub(r"```(?:json)?", "", text).strip().rstrip("`").strip()
    return json.loads(text)


# ─────────────────────────────────────────────────────────────
# Groq — Summarisation
# ─────────────────────────────────────────────────────────────

def _groq_summarise_batch(articles: list[dict]) -> list[dict]:
    items = []
    for i, a in enumerate(articles):
        snippet = (a.get("description") or a.get("title") or "")[:300]
        items.append(f'{i+1}. TITLE: {a["title"]}\n   SNIPPET: {snippet}')

    prompt = (
        "You are a factual news summariser. For each article below, "
        "provide a 2-3 sentence objective summary and 3-5 relevant tags.\n\n"
        "Return ONLY a JSON array (no markdown, no explanation):\n"
        '[{"summary": "...", "tags": ["tag1", "tag2", "tag3"]}, ...]\n\n'
        "Articles:\n" + "\n\n".join(items)
    )

    try:
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1200,
            temperature=0.2,
        )
        raw = response.choices[0].message.content or ""
        parsed = _extract_json(raw)
        if isinstance(parsed, list) and len(parsed) == len(articles):
            return parsed
        raise ValueError(f"Length mismatch: expected {len(articles)}, got {len(parsed)}")
    except Exception as exc:
        logger.warning("Groq batch failed: %s -- using fallback", exc)
        return [
            {"summary": (a.get("description") or a.get("title") or "")[:200], "tags": []}
            for a in articles
        ]


# ─────────────────────────────────────────────────────────────
# Gemini — Categorisation
# ─────────────────────────────────────────────────────────────

def _gemini_categorise_batch(articles: list[dict]) -> list[dict]:
    items = []
    for i, a in enumerate(articles):
        region_hint = "INDIA" if a.get("region") == "india" else "WORLD"
        items.append(f'{i+1}. [{region_hint}] {a["title"]}')

    valid_cats = ", ".join(sorted(VALID_CATEGORIES))
    prompt = (
        f"You are a news categorisation engine. Valid categories: {valid_cats}.\n\n"
        "For each article, return ONLY a JSON array (no markdown):\n"
        '[{"category": "...", "subcategory": "...", "is_india_focused": true/false, '
        '"verification_status": "confirmed"|"flagged"|"unverified", "trend_score": 0-100}]\n\n'
        "Rules:\n"
        "- category must be exactly one value from the valid list\n"
        "- subcategory: specific 1-3 word topic (e.g. Artificial Intelligence, Cricket)\n"
        "- verification_status: confirmed=hard fact, flagged=opinion/satire, unverified=default\n"
        "- trend_score: 0-100 based on newsworthiness right now\n\n"
        "Articles:\n" + "\n".join(items)
    )

    try:
        response = gemini_client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.1, max_output_tokens=1000),
        )
        raw = response.text or ""
        parsed = _extract_json(raw)
        if isinstance(parsed, list) and len(parsed) == len(articles):
            for item in parsed:
                if item.get("category") not in VALID_CATEGORIES:
                    item["category"] = "World Affairs"
                item["trend_score"] = max(0, min(100, int(item.get("trend_score", 30))))
                if item.get("verification_status") not in {"confirmed", "flagged", "unverified"}:
                    item["verification_status"] = "unverified"
            return parsed
        raise ValueError(f"Length mismatch: expected {len(articles)}, got {len(parsed)}")
    except Exception as exc:
        logger.warning("Gemini batch failed: %s -- using defaults", exc)
        return [
            {
                "category":            a.get("category", "World Affairs"),
                "subcategory":         None,
                "is_india_focused":    a.get("region") == "india",
                "verification_status": a.get("verification_status", "unverified"),
                "trend_score":         20,
            }
            for a in articles
        ]


# ─────────────────────────────────────────────────────────────
# Main processing pipeline
# ─────────────────────────────────────────────────────────────

async def process_articles(articles: list[dict]) -> list[dict]:
    processed: list[dict] = []
    for i in range(0, len(articles), BATCH_SIZE):
        # Stop AI processing if we've hit the daily cap
        if i // BATCH_SIZE >= MAX_AI_BATCHES_PER_RUN:
            logger.warning("Daily AI batch cap reached (%d batches). Saving remaining articles with fallback.", MAX_AI_BATCHES_PER_RUN)
            # Save remaining articles with raw descriptions, no AI
            for article in articles[i:]:
                processed.append({
                    "title":               article["title"],
                    "summary":             (article.get("description") or article.get("title") or "")[:200],
                    "source_url":          article["source_url"],
                    "source_name":         article["source_name"],
                    "image_url":           article.get("image_url"),
                    "category":            article.get("category", "World Affairs"),
                    "subcategory":         None,
                    "is_india_focused":    article.get("region") == "india",
                    "language":            "en",
                    "trend_score":         10,
                    "verification_status": "unverified",
                    "source_count":        article.get("source_count", 1),
                    "published_at":        article.get("published_at"),
                    "tags":                [],
                    "related_sources":     article.get("related_sources", []),
                    "translations":        {},
                })
            break

        batch = articles[i : i + BATCH_SIZE]

    for i in range(0, len(articles), BATCH_SIZE):
        batch = articles[i : i + BATCH_SIZE]

        loop = asyncio.get_event_loop()
        summaries, categories = await asyncio.gather(
            loop.run_in_executor(None, _groq_summarise_batch, batch),
            loop.run_in_executor(None, _gemini_categorise_batch, batch),
        )

        for article, summary_data, cat_data in zip(batch, summaries, categories):
            trend_score = cat_data.get("trend_score", 20) + article.get("trend_boost", 0)

            existing_status = article.get("verification_status", "unverified")
            ai_status = cat_data.get("verification_status", "unverified")
            STATUS_RANK = {"confirmed": 2, "unverified": 1, "flagged": 0}
            final_status = (
                existing_status
                if STATUS_RANK.get(existing_status, 0) >= STATUS_RANK.get(ai_status, 0)
                else ai_status
            )

            processed.append({
                "title":               article["title"],
                "summary":             summary_data.get("summary", ""),
                "source_url":          article["source_url"],
                "source_name":         article["source_name"],
                "image_url":           article.get("image_url"),
                "category":            cat_data.get("category", "World Affairs"),
                "subcategory":         cat_data.get("subcategory"),
                "is_india_focused":    cat_data.get("is_india_focused", False),
                "language":            "en",
                "trend_score":         min(100, trend_score),
                "verification_status": final_status,
                "source_count":        article.get("source_count", 1),
                "published_at":        article.get("published_at"),
                "tags":                summary_data.get("tags", []),
                "related_sources":     article.get("related_sources", []),
                "translations":        {},
            })

        logger.info("Processed batch %d/%d (%d articles done)",
                    i // BATCH_SIZE + 1, -(-len(articles) // BATCH_SIZE), len(processed))
        await asyncio.sleep(1.0)

    return processed


# ─────────────────────────────────────────────────────────────
# Trending topics regeneration (hourly)
# ─────────────────────────────────────────────────────────────

def generate_trending_topics(recent_titles: list[str]) -> list[dict]:
    if not recent_titles:
        return []
    titles_text = "\n".join(f"{i+1}. {t}" for i, t in enumerate(recent_titles[:50]))
    prompt = (
        "From these headlines, extract the top 8 trending topics right now.\n"
        "Return ONLY a JSON array:\n"
        '[{"topic": "Short topic name", "score": 0.0-1.0, "article_count": integer}]\n\n'
        "Headlines:\n" + titles_text
    )
    try:
        response = gemini_client.models.generate_content(model=GEMINI_MODEL, contents=prompt)
        return _extract_json(response.text or "")[:8]
    except Exception as exc:
        logger.error("Trending topics generation failed: %s", exc)
    return []


# ─────────────────────────────────────────────────────────────
# On-demand translation
# ─────────────────────────────────────────────────────────────

LANGUAGE_NAMES = {
    "hi": "Hindi", "ta": "Tamil", "te": "Telugu",
    "ml": "Malayalam", "bn": "Bengali", "mr": "Marathi", "kn": "Kannada",
}

def translate_article(title: str, summary: str, target_lang: str) -> dict:
    lang_name = LANGUAGE_NAMES.get(target_lang, target_lang)
    prompt = (
        f"Translate into {lang_name}. Return ONLY JSON (no markdown):\n"
        '{"title": "...", "summary": "..."}\n\n'
        f"TITLE: {title}\nSUMMARY: {summary}"
    )
    response = gemini_client.models.generate_content(model=GEMINI_MODEL, contents=prompt)
    return _extract_json(response.text or "")