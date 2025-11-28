import hashlib
import os
import json

CACHE_FILE = "used_quotes.json"

def load_cache():
    if not os.path.exists(CACHE_FILE):
        return set()
    with open(CACHE_FILE, "r") as f:
        return set(json.load(f))

def save_cache(cache):
    with open(CACHE_FILE, "w") as f:
        json.dump(list(cache), f)

def hash_quote(q):
    return hashlib.sha256(q.encode()).hexdigest()

def not_used_before(q):
    h = hash_quote(q)
    cache = load_cache()
    if h in cache:
        return False
    cache.add(h)
    save_cache(cache)
    return True
