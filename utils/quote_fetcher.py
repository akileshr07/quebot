import requests
import random
import time
import os
from .dedupe_cache import not_used_before

API_KEY = os.getenv("X_API_KEY")

CATEGORIES = [
    "wisdom", "life", "success", "courage", "faith",
    "happiness", "inspirational", "truth", "love",
]

def fetch_quote():
    for attempt in range(3):  # retry-safe
        try:
            category = ",".join(random.sample(CATEGORIES, 2))
            url = f"https://api.api-ninjas.com/v2/quotes?categories={category}"
            headers = {"X-Api-Key": API_KEY}

            res = requests.get(url, headers=headers, timeout=10)
            data = res.json()[0]

            quote = f"{data['quote']} — {data['author']}"

            if not_used_before(quote):
                return quote
            
        except Exception:
            time.sleep(2)

    return None
