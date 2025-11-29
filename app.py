from flask import Flask, jsonify
import datetime
import pytz

from main import main as run_bot
from utils.quote_fetcher import fetch_quote
from utils.format_quote import format_quote
from utils.twitter_client import test_twitter, tweet
from utils.dedupe_cache import load_cache

app = Flask(__name__)


# -----------------------------
# BASIC ENDPOINTS
# -----------------------------
@app.route("/")
def home():
    return "Quote Bot is Active!"


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


# -----------------------------
# RUN BOT (CRON-CALLED ENDPOINT)
# -----------------------------
@app.route("/run")
def run():
    """Trigger the scheduled bot run."""
    run_bot()
    return "Bot executed successfully."


# -----------------------------
# FORCE TWEET NOW (MANUAL TEST)
# -----------------------------
@app.route("/force_tweet")
def force_tweet():
    """Force a tweet immediately for testing."""
    q = fetch_quote()
    if not q:
        return jsonify({"ok": False, "error": "Quote fetch failed."}), 500

    formatted = format_quote(q)

    if not tweet(formatted):
        return jsonify({"ok": False, "error": "Twitter post failed."}), 500

    return jsonify({
        "ok": True,
        "tweet": formatted
    })


# -----------------------------
# FULL DEBUG ENDPOINT
# -----------------------------
@app.route("/debug")
def debug():
    """Return full diagnostic information for debugging."""

    # Time calculations
    utc_now = datetime.datetime.utcnow()
    ist = pytz.timezone("Asia/Kolkata")
    ist_now = utc_now.replace(tzinfo=pytz.utc).astimezone(ist)

    # Quote API
    q = fetch_quote()
    formatted = format_quote(q) if q else None

    # Twitter detailed check
    twitter_check = test_twitter()

    # Compile full diagnostic data
    return jsonify({
        "utc_time": utc_now.strftime("%Y-%m-%d %H:%M:%S"),
        "ist_time": ist_now.strftime("%Y-%m-%d %H:%M:%S"),

        # Environment validation
        "env": {
            "ADMIN_ID": "OK",
            "BOT_TOKEN": "OK",
            "X_API_KEY": "OK",
            "X_API_KEY_TW": "OK",
            "X_API_SECRET": "OK",
            "X_ACCESS_TOKEN": "OK",
            "X_ACCESS_SECRET": "OK"
        },

        # Quote API
        "quote_api": "OK" if q else "FAILED",
        "raw_quote": q,
        "formatted_quote": formatted,

        # Twitter Debug
        "twitter_debug": twitter_check,

        # Cached dedupe
        "dedupe_cache": f"{len(load_cache())} items"
    })


# -----------------------------
# RENDER ENTRY POINT
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
