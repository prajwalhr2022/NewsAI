# ============================================================
# processor.py — News AI processing
# Groq: summarisation | Gemini: categorisation + verification
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

groq_client   = Groq(api_key=os.environ["GROQ_API_KEY"])
gemini_client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
GEMINI_MODEL  = "gemini-2.0-flash"

BATCH_SIZE = 5

# ── Expanded category list ────────────────────────────────────
VALID_CATEGORIES = {
    "Politics",
    "Geopolitics",
    "Regional Politics",
    "Technology",
    "Business & Economy",
    "Trade & Markets",
    "Agriculture",
    "Sports",
    "Cricket",
    "Science & Space",
    "Health & Medicine",
    "Entertainment",
    "Environment & Climate",
    "World Affairs",
    "Crime & Law",
    "Education",
    "Lifestyle",
    "Defence & Security",
    "Cars & Automobiles",
    "Electronics & Gadgets",
}

# ── Junk/spam article detection ───────────────────────────────
JUNK_PATTERNS = [
    r"click here", r"subscribe now", r"sign up for",
    r"buy now", r"limited offer", r"exclusive deal",
    r"casino", r"betting", r"forex trading",
    r"lose weight", r"miracle cure", r"earn \$",
    r"sponsored", r"advertisement", r"press release",
    r"follow us on", r"join our newsletter",
]

def is_junk_article(title: str, description: str) -> bool:
    """Return True if article looks like spam/ad/junk."""
    combined = (title + " " + (description or "")).lower()
    # Too short title
    if len(title.strip()) < 10:
        return True
    # Junk patterns
    for pattern in JUNK_PATTERNS:
        if re.search(pattern, combined):
            return True
    # All caps title (usually clickbait)
    if title == title.upper() and len(title) > 20:
        return True
    return False


def _extract_json(text: str) -> Any:
    text = re.sub(r"```(?:json)?", "", text).strip().rstrip("`").strip()
    return json.loads(text)


# ── Groq — summarisation ──────────────────────────────────────

def _groq_summarise_batch(articles: list[dict]) -> list[dict]:
    items = []
    for i, a in enumerate(articles):
        snippet = (a.get("description") or a.get("title") or "")[:300]
        items.append(f'{i+1}. TITLE: {a["title"]}\n   SNIPPET: {snippet}')

    prompt = (
        "You are a factual news summariser for a professional news site called Satyaksh. "
        "For each article below, provide a 2-3 sentence objective factual summary and 3-5 relevant tags.\n\n"
        "Return ONLY a JSON array (no markdown):\n"
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


# ── Gemini — categorisation + verification ───────────────────

def _gemini_categorise_batch(articles: list[dict]) -> list[dict]:
    items = []
    for i, a in enumerate(articles):
        region_hint = "INDIA" if a.get("region") == "india" else "WORLD"
        snippet = (a.get("description") or "")[:100]
        items.append(f'{i+1}. [{region_hint}] {a["title"]} | {snippet}')

    valid_cats = ", ".join(sorted(VALID_CATEGORIES))
    prompt = (
        f"You are a news categorisation engine for NewsAI news site.\n"
        f"Valid categories: {valid_cats}\n\n"
        "For each article return ONLY a JSON array (no markdown):\n"
        "[\n"
        '  {\n'
        '    "category": "<from valid list above>",\n'
        '    "subcategory": "<specific 1-3 word subtopic>",\n'
        '    "is_india_focused": true/false,\n'
        '    "verification_status": "confirmed"|"unverified"|"flagged",\n'
        '    "is_genuine_news": true/false,\n'
        '    "trend_score": <0-100>\n'
        '  }\n'
        "]\n\n"
        "Rules:\n"
        "- category MUST be exactly one value from the valid list\n"
        "- subcategory: specific topic like 'Lok Sabha', 'iPhone 16', 'Champions League'\n"
        "- verification_status:\n"
        "    confirmed = reported by multiple major outlets or official sources\n"
        "    flagged = opinion, satire, unverified claim, or dubious source\n"
        "    unverified = single source, not yet confirmed elsewhere\n"
        "- is_genuine_news: false if this looks like sponsored content, ad, listicle, or non-news\n"
        "- trend_score: 0-100 based on newsworthiness and importance right now\n\n"
        "Articles:\n" + "\n".join(items)
    )

    try:
        response = gemini_client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.1, max_output_tokens=1200),
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
        raise ValueError(f"Length mismatch: {len(articles)} vs {len(parsed)}")
    except Exception as exc:
        logger.warning("Gemini batch failed: %s -- using defaults", exc)
        return [
            {
                "category":            a.get("category", "World Affairs"),
                "subcategory":         None,
                "is_india_focused":    a.get("region") == "india",
                "verification_status": "unverified",
                "is_genuine_news":     True,
                "trend_score":         20,
            }
            for a in articles
        ]


# ── Main processing pipeline ──────────────────────────────────

async def process_articles(articles: list[dict]) -> list[dict]:
    # Pre-filter obvious junk before sending to AI
    clean_articles = []
    for a in articles:
        if is_junk_article(a["title"], a.get("description", "")):
            logger.debug("Filtered junk article: %s", a["title"][:60])
            continue
        clean_articles.append(a)

    logger.info("After junk filter: %d/%d articles remain", len(clean_articles), len(articles))

    processed: list[dict] = []

    for i in range(0, len(clean_articles), BATCH_SIZE):
        batch = clean_articles[i: i + BATCH_SIZE]

        loop = asyncio.get_event_loop()
        summaries, categories = await asyncio.gather(
            loop.run_in_executor(None, _groq_summarise_batch, batch),
            loop.run_in_executor(None, _gemini_categorise_batch, batch),
        )

        for article, summary_data, cat_data in zip(batch, summaries, categories):
            # Skip AI-flagged non-genuine articles
            if not cat_data.get("is_genuine_news", True):
                logger.debug("Skipping non-genuine: %s", article["title"][:60])
                continue

            trend_score = cat_data.get("trend_score", 20) + article.get("trend_boost", 0)

            # Verification: honour dedup-based upgrades
            existing_status = article.get("verification_status", "unverified")
            ai_status       = cat_data.get("verification_status", "unverified")
            STATUS_RANK     = {"confirmed": 2, "unverified": 1, "flagged": 0}
            final_status    = (
                existing_status
                if STATUS_RANK.get(existing_status, 0) >= STATUS_RANK.get(ai_status, 0)
                else ai_status
            )

            # Auto-confirm if 3+ sources reported it
            if article.get("source_count", 1) >= 3:
                final_status = "confirmed"
            elif article.get("source_count", 1) >= 2 and article.get("tier", 2) == 1:
                final_status = "confirmed"

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
                    i // BATCH_SIZE + 1, -(-len(clean_articles) // BATCH_SIZE), len(processed))
        await asyncio.sleep(1.0)

    return processed


# ── Trending topics ───────────────────────────────────────────

def generate_trending_topics(recent_titles: list[str]) -> list[dict]:
    if not recent_titles:
        return []
    titles_text = "\n".join(f"{i+1}. {t}" for i, t in enumerate(recent_titles[:50]))
    prompt = (
        "From these news headlines, extract the top 8 trending topics right now.\n"
        "Return ONLY a JSON array:\n"
        '[{"topic": "Short topic name", "score": 0.0-1.0, "article_count": integer}]\n\n'
        "Headlines:\n" + titles_text
    )
    try:
        response = gemini_client.models.generate_content(model=GEMINI_MODEL, contents=prompt)
        return _extract_json(response.text or "")[:8]
    except Exception as exc:
        logger.error("Trending topics failed: %s", exc)
    return []


# ── Predictions ───────────────────────────────────────────────

def generate_predictions(recent_titles: list[str]) -> dict:
    """
    Generate 1-week market predictions based on recent news.
    Returns dict with gold, silver, oil, global_stocks, india_stocks predictions.
    """
    if not recent_titles:
        return {}
    titles_text = "\n".join(f"{i+1}. {t}" for i, t in enumerate(recent_titles[:60]))
    prompt = (
        "You are a financial analyst. Based on the following recent news headlines, "
        "provide brief 1-week outlook predictions.\n\n"
        "Return ONLY a JSON object (no markdown):\n"
        "{\n"
        '  "gold":          {"direction": "up"|"down"|"sideways", "reason": "1 sentence", "confidence": "high"|"medium"|"low"},\n'
        '  "silver":        {"direction": "up"|"down"|"sideways", "reason": "1 sentence", "confidence": "high"|"medium"|"low"},\n'
        '  "oil":           {"direction": "up"|"down"|"sideways", "reason": "1 sentence", "confidence": "high"|"medium"|"low"},\n'
        '  "global_stocks": {"direction": "up"|"down"|"sideways", "reason": "1 sentence", "confidence": "high"|"medium"|"low"},\n'
        '  "india_stocks":  {"direction": "up"|"down"|"sideways", "reason": "1 sentence", "confidence": "high"|"medium"|"low"},\n'
        '  "generated_at":  "ISO timestamp"\n'
        "}\n\n"
        "Recent headlines:\n" + titles_text
    )
    try:
        response = gemini_client.models.generate_content(model=GEMINI_MODEL, contents=prompt)
        result = _extract_json(response.text or "")
        from datetime import datetime, timezone
        result["generated_at"] = datetime.now(timezone.utc).isoformat()
        return result
    except Exception as exc:
        logger.error("Predictions generation failed: %s", exc)
    return {}


# ── On-demand translation ─────────────────────────────────────

LANGUAGE_NAMES = {"hi": "Hindi", "kn": "Kannada"}

def translate_article(title: str, summary: str, target_lang: str) -> dict:
    lang_name = LANGUAGE_NAMES.get(target_lang, target_lang)
    prompt = (
        f"Translate into {lang_name}. Return ONLY JSON (no markdown):\n"
        '{"title": "...", "summary": "..."}\n\n'
        f"TITLE: {title}\nSUMMARY: {summary}"
    )
    response = gemini_client.models.generate_content(model=GEMINI_MODEL, contents=prompt)
    return _extract_json(response.text or "")
