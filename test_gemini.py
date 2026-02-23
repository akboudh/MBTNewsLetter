#!/usr/bin/env python3
"""
Test script to verify Gemini API is working.
Uses GEMINI_API_KEY from .env to send a short prompt via REST and print the response.
"""
import sys

def main():
    from dotenv import load_dotenv
    load_dotenv()
    import os
    api_key = os.getenv("GEMINI_API_KEY")
    model_name = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

    if not api_key:
        print("FAIL: GEMINI_API_KEY not set in .env")
        sys.exit(1)

    import requests
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent"
    payload = {
        "contents": [{"parts": [{"text": "Reply in one short sentence: confirm you are working."}]}],
        "generationConfig": {"temperature": 0.3, "maxOutputTokens": 100},
    }
    print(f"Testing Gemini (model={model_name}, timeout=30s)...")
    try:
        r = requests.post(url, params={"key": api_key}, json=payload, timeout=30)
        r.raise_for_status()
        data = r.json()
        candidates = data.get("candidates") or []
        if not candidates:
            print("FAIL: No candidates in response")
            sys.exit(1)
        parts = candidates[0].get("content", {}).get("parts") or []
        if not parts:
            print("FAIL: Empty content in response")
            sys.exit(1)
        text = (parts[0].get("text") or "").strip()
        if not text:
            print("FAIL: Empty text in response")
            sys.exit(1)
        print("OK: Gemini is working.")
        print("Response:", text)
        sys.exit(0)
    except requests.exceptions.Timeout:
        print("FAIL: Request timed out after 30s")
        sys.exit(1)
    except requests.exceptions.HTTPError as e:
        code = e.response.status_code if e.response else None
        err = e.response.text if e.response is not None else str(e)
        if code == 429:
            print("FAIL: 429 Quota exceeded. Check plan/billing at https://ai.google.dev/gemini-api")
        else:
            print("FAIL:", code or "HTTP error", err[:200])
        sys.exit(1)
    except Exception as e:
        print("FAIL:", e)
        sys.exit(1)

if __name__ == "__main__":
    main()
