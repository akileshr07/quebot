import hashlib
import os
import json

CACHE_FILE = "used_quotes.json"

def load_cache():
    if not os.path.exists(CACHE_FILE):
        return set()
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return set(json.load(f))
    except Exception:
        return set()

def save_cache(cache):
    try:
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(list(cache), f, ensure_ascii=False)
    except Exception:
        pass

def hash_quote(q):
    return hashlib.sha256(q.encode("utf-8")).hexdigest()

def not_used_before(q):
    """
    Return True if quote was not used before and mark it used.
    """
    h = hash_quote(q)
    cache = load_cache()
    if h in cache:
        return False
    cache.add(h)
    save_cache(cache)
    return True
