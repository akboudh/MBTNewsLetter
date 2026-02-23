"""
Gemini API client for newsletter generation.
Uses REST API with requests + timeout (same as test_gemini.py) so the call completes reliably.
Single env var GEMINI_API_KEY. Model: gemini-2.0-flash. Single turn: system prompt + user message.
"""
import logging
import requests
from config import GEMINI_API_KEY, GEMINI_MODEL, SYSTEM_PROMPT

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

GEMINI_BASE = "https://generativelanguage.googleapis.com/v1beta"
GEMINI_TIMEOUT_SEC = 60


def _build_user_prompt(scraped_items: list, days_since_last_run: int) -> str:
    """Build the user prompt from scraped items."""
    items_text = []
    for item in scraped_items:
        if item.get("success"):
            items_text.append({
                "source": item["url"],
                "content": item["text"][:2000],
                "articles": item.get("articles", [])[:5],
            })
    return f"""Analyze these tech news sources from the past {days_since_last_run} days. Find the 3-4 stories with the deepest strategic implications for someone building a career in business + AI.

SOURCES:

{str(items_text)}

Focus on:

- What's genuinely NEW or SURPRISING (not just incremental updates)

- Stories that reveal competitive dynamics or market shifts

- Developments that create opportunities for students/professionals

- Insights that challenge conventional thinking

Be ruthless: Skip stories that are surface-level or already widely understood."""


def generate_newsletter(scraped_items: list, days_since_last_run: int = 5) -> str:
    """Generate newsletter content using Gemini REST API. Single turn: system + user message."""
    if not GEMINI_API_KEY:
        raise ValueError(
            "GEMINI_API_KEY not set in environment variables. Add it to your .env file."
        )

    user_prompt = _build_user_prompt(scraped_items, days_since_last_run)
    url = f"{GEMINI_BASE}/models/{GEMINI_MODEL}:generateContent"
    payload = {
        "contents": [{"parts": [{"text": user_prompt}]}],
        "systemInstruction": {"parts": [{"text": SYSTEM_PROMPT}]},
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 2000,
        },
    }

    logger.info("Calling Gemini API (model=%s, timeout=%ds)...", GEMINI_MODEL, GEMINI_TIMEOUT_SEC)
    r = requests.post(
        url,
        params={"key": GEMINI_API_KEY},
        json=payload,
        timeout=GEMINI_TIMEOUT_SEC,
        headers={"Content-Type": "application/json"},
    )
    r.raise_for_status()
    data = r.json()
    candidates = data.get("candidates") or []
    if not candidates:
        raise ValueError("Gemini returned no candidates")
    parts = candidates[0].get("content", {}).get("parts") or []
    if not parts:
        raise ValueError("Gemini returned empty content")
    text = (parts[0].get("text") or "").strip()
    if not text:
        raise ValueError("Gemini returned empty text")
    logger.info("Newsletter generated successfully (model=%s)", GEMINI_MODEL)
    return text
