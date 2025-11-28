import requests
import random
import time
import os
from .dedupe_cache import not_used_before

API_KEY = os.getenv("X_API_KEY")

CATEGORIES = [
    "wisdom", "life", "success", "courage", "faith",
    "happiness", "inspirational", "truth", "love",
    "humor", "leadership", "nature", "time", "freedom"
]

def fetch_quote(max_retries=3):
    """
    Returns dict: {"quote": text, "author": author or "", "categories": [..]}
    Returns None on failure or if duplicate after retries.
    """
    for attempt in range(max_retries):
        try:
            # pick 1-2 categories to improve relevance
            cats = ",".join(random.sample(CATEGORIES, k=random.choice([1,2])))
            url = f"https://api.api-ninjas.com/v2/quotes?categories={cats}"
            headers = {"X-Api-Key": API_KEY}
            res = requests.get(url, headers=headers, timeout=10)
            res.raise_for_status()
            data = res.json()
            if not data:
                time.sleep(1)
                continue
            item = data[0]
            quote_text = item.get("quote", "").strip()
            author = item.get("author", "") or ""
            categories = item.get("categories", []) or (cats.split(",") if cats else [])

            full = f"{quote_text} — {author}" if author else quote_text
            # skip duplicates
            if not_used_before(full):
                return {"quote": quote_text, "author": author, "categories": categories}
            # else try again to get non-duplicate
            time.sleep(0.5)
        except Exception:
            time.sleep(1)
    return None
