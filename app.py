from flask import Flask, jsonify
from main import main as run_bot
from utils.twitter_client import test_connection
from utils.quote_fetcher import fetch_quote
from utils.format_quote import format_quote
from utils.dedupe_cache import load_cache
import datetime, pytz, os

app = Flask(__name__)

@app.route("/")
def home():
    return "Quote Bot is Active!"

@app.route("/run")
def run():
    return jsonify(run_bot())

@app.route("/debug")
def debug():
    utc_now = datetime.datetime.utcnow()
    ist = pytz.timezone("Asia/Kolkata")
    ist_now = utc_now.replace(tzinfo=pytz.utc).astimezone(ist)

    q = fetch_quote()
    formatted = format_quote(q) if q else None
    tw = test_connection()

    env_status = {
        "X_API_KEY_TW": "OK" if os.getenv("X_API_KEY_TW") else "MISSING",
        "X_API_SECRET": "OK" if os.getenv("X_API_SECRET") else "MISSING",
        "X_ACCESS_TOKEN": "OK" if os.getenv("X_ACCESS_TOKEN") else "MISSING",
        "X_ACCESS_SECRET": "OK" if os.getenv("X_ACCESS_SECRET") else "MISSING"
    }

    return jsonify({
        "utc_time": utc_now.strftime("%Y-%m-%d %H:%M:%S"),
        "ist_time": ist_now.strftime("%Y-%m-%d %H:%M:%S"),
        "env_loaded": env_status,
        "raw_quote": q,
        "formatted_quote": formatted,
        "quote_api": "OK" if q else "FAILED",
        "twitter_debug": tw,
        "dedupe_cache": f"{len(load_cache())} items"
    })
