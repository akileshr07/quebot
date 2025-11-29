from flask import Flask, jsonify
from main import main as run_bot
from utils.quote_fetcher import fetch_quote
from utils.format_quote import format_quote
from utils.twitter_client import test_twitter
from utils.dedupe_cache import load_cache

app = Flask(__name__)

@app.route("/")
def home():
    return "Quote Bot is Active!"

@app.route("/debug")
def debug():
    import datetime
    import pytz, os

    utc_now = datetime.datetime.utcnow()
    ist = pytz.timezone("Asia/Kolkata")
    ist_now = utc_now.replace(tzinfo=pytz.utc).astimezone(ist)

    q = fetch_quote()
    formatted = format_quote(q) if q else None
    twitter_check = test_twitter()

    return jsonify({
        "utc_time": utc_now.strftime("%Y-%m-%d %H:%M:%S"),
        "ist_time": ist_now.strftime("%Y-%m-%d %H:%M:%S"),
        "twitter_debug": twitter_check,
        "quote_api": "OK" if q else "FAILED",
        "raw_quote": q,
        "formatted_quote": formatted,
        "dedupe_cache": f"{len(load_cache())} items"
    })
