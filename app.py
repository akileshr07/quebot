from flask import Flask, jsonify
from main import main as run_bot
from utils.quote_fetcher import fetch_quote
from utils.format_quote import format_quote
from utils.twitter_client import test_twitter
from utils.dedupe_cache import load_cache
import datetime
import pytz
import os

app = Flask(__name__)


# ------------------------------------------------------
# ROOT ENDPOINT — service alive
# ------------------------------------------------------
@app.route("/")
def home():
    return "Quote Bot is Active!"


# ------------------------------------------------------
# RUN ENDPOINT — manual bot execution
# ------------------------------------------------------
@app.route("/run")
def run():
    try:
        run_bot()
        return "Bot executed successfully."
    except Exception as e:
        return f"Bot failed: {str(e)}", 500


# ------------------------------------------------------
# DEBUG ENDPOINT — FULL DIAGNOSTICS
# ------------------------------------------------------
@app.route("/debug")
def debug():
    """Deep diagnostics: API keys, quote API, formatting,
    dedupe status, and FULL Twitter diagnostics including:
    - auth_ok
    - write_ok
    - account details
    - raw error message
    - error type
    """

    # Time info
    utc_now = datetime.datetime.utcnow()
    ist = pytz.timezone("Asia/Kolkata")
    ist_now = utc_now.replace(tzinfo=pytz.utc).astimezone(ist)

    # Fetch quote for debug
    quote = fetch_quote()
    formatted = format_quote(quote) if quote else None

    # Run full twitter diagnostic
    twitter_status = test_twitter()

    # Build debug info
    data = {
        "utc_time": utc_now.strftime("%Y-%m-%d %H:%M:%S"),
        "ist_time": ist_now.strftime("%Y-%m-%d %H:%M:%S"),

        # ENV PRESENT CHECK
        "env_loaded": {
            "ADMIN_ID": "OK" if os.getenv("ADMIN_ID") else "MISSING",
            "BOT_TOKEN": "OK" if os.getenv("BOT_TOKEN") else "MISSING",
            "X_API_KEY": "OK" if os.getenv("X_API_KEY") else "MISSING",
            "X_API_KEY_TW": "OK" if os.getenv("X_API_KEY_TW") else "MISSING",
            "X_API_SECRET": "OK" if os.getenv("X_API_SECRET") else "MISSING",
            "X_ACCESS_TOKEN": "OK" if os.getenv("X_ACCESS_TOKEN") else "MISSING",
            "X_ACCESS_SECRET": "OK" if os.getenv("X_ACCESS_SECRET") else "MISSING"
        },

        # Quote API
        "quote_api": "OK" if quote else "FAILED",
        "raw_quote": quote,
        "formatted_quote": formatted,

        # Cache info
        "dedupe_cache": f"{len(load_cache())} items",

        # FULL Twitter diagnostics
        "twitter_debug": twitter_status
    }

    return jsonify(data)


# ------------------------------------------------------
# FORCE POST ENDPOINT — bypass time restriction
# ------------------------------------------------------
@app.route("/force_tweet")
def force_tweet():
    """Posts a real quote immediately — no hour restrictions.
    Useful for live testing Tweet posting."""
    try:
        q = fetch_quote()
        if not q:
            return "Failed to fetch quote.", 500

        formatted = format_quote(q)

        from utils.twitter_client import tweet
        ok = tweet(formatted)

        if ok:
            return "Tweet posted successfully."
        return "Tweet failed to post.", 500

    except Exception as e:
        return f"Force tweet error: {str(e)}", 500


# ------------------------------------------------------
# MAIN SERVER START
# ------------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
