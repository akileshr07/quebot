from utils.quote_fetcher import fetch_quote
from utils.format_quote import format_quote
from utils.twitter_client import post_tweet
from utils.dedupe_cache import is_duplicate, add_to_cache

def main():
    q = fetch_quote()
    if not q:
        return {"success": False, "error": "Quote API failure"}

    if is_duplicate(q["quote"]):
        return {"success": False, "error": "Duplicate quote skipped"}

    formatted = format_quote(q)

    posted = post_tweet(formatted)

    if posted:
        add_to_cache(q["quote"])
        return {"success": True, "tweet": formatted}
    else:
        return {"success": False, "error": "Tweet failed"}
