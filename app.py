from flask import Flask
import datetime
import os
import json

from main import main as run_bot
from utils.quote_fetcher import fetch_quote
from utils.format_quote import format_quote
from utils.twitter_client import tweet
from utils.telegram_logger import log_telegram

app = Flask(__name__)

@app.route("/")
def home():
    return "Quote Bot is Active!"

@app.route("/run")
def run():
    run_bot()
    return "Bot executed successfully."

@app.route("/debug")
def debug():

    report = {}
    now_utc = datetime.datetime.utcnow()
    now_ist = now_utc + datetime.timedelta(hours=5, minutes=30)

    # TIME INFO
    report["utc_time"] = now_utc.strftime("%Y-%m-%d %H:%M:%S")
    report["ist_time"] = now_ist.strftime("%Y-%m-%d %H:%M:%S")

    # ENV CHECK
    env_vars = [
        "ADMIN_ID", "BOT_TOKEN",
        "X_API_KEY", "X_API_KEY_TW",
        "X_API_SECRET", "X_ACCESS_TOKEN",
        "X_ACCESS_SECRET",
    ]

    report["env_loaded"] = {key: ("OK" if os.getenv(key) else "MISSING") for key in env_vars}

    # QUOTE API TEST
    try:
        q = fetch_quote()
        report["quote_api"] = "OK" if q else "FAILED"
        if q:
            report["raw_quote"] = q
    except Exception as e:
        report["quote_api"] = f"ERROR: {str(e)}"

    # FORMAT TEST
    try:
        if q:
            formatted = format_quote(q)
            report["formatted_quote"] = formatted
    except Exception as e:
        report["format_error"] = str(e)

    # TWITTER TEST
    try:
        test_text = "Debug Tweet Test " + now_utc.strftime("%H:%M:%S")
        test_post = tweet(test_text)
        report["twitter_test"] = "SUCCESS" if test_post else "FAILED"
    except Exception as e:
        report["twitter_test"] = f"ERROR: {str(e)}"

    # TELEGRAM TEST
    try:
        tg = log_telegram("Debug: Telegram test message.")
        report["telegram_test"] = "SENT"
    except Exception as e:
        report["telegram_test"] = f"ERROR: {str(e)}"

    # Dedupe file check
    try:
        if os.path.exists("used_quotes.json"):
            with open("used_quotes.json", "r") as f:
                data = json.load(f)
            report["dedupe_cache"] = f"{len(data)} items"
        else:
            report["dedupe_cache"] = "NO FILE"
    except Exception as e:
        report["dedupe_cache"] = f"ERROR: {str(e)}"

    # Return readable JSON
    return json.dumps(report, indent=4)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
