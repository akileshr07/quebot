import datetime
import pytz
from utils.quote_fetcher import fetch_quote, fetch_image
from utils.twitter_client import tweet_image
from utils.telegram_logger import log_telegram
from utils.format_quote import format_quote
from utils.dedupe_cache import not_used_before

def main():
    ist = pytz.timezone("Asia/Kolkata")
    now_ist = datetime.datetime.now(ist)
    hour = now_ist.hour

    response = {
        "time": now_ist.strftime("%Y-%m-%d %H:%M:%S"),
        "hour": hour,
        "tweet_attempt": False,
        "tweet_status": None,
        "quote": None
    }

    # allowed posting time
    if not (6 <= hour <= 21):
        response["tweet_status"] = "Outside posting hours"
        return response

    # fetch quote text (this becomes caption)
    q = fetch_quote()
    if not q:
        log_telegram("Quote bot: Failed to fetch a new quote.")
        response["tweet_status"] = "Quote fetch failed"
        return response

    # format the quote (for caption)
    formatted = format_quote(q)
    if not formatted:
        log_telegram("Quote bot: Formatting failed.")
        response["tweet_status"] = "Formatting failed"
        return response

    # check duplicate by caption
    if not not_used_before(formatted):
        log_telegram("Duplicate quote skipped.")
        response["tweet_status"] = "Duplicate detected"
        return response

    # fetch image from API
    img = fetch_image()
    if not img:
        log_telegram("Quote bot: Image fetch failed.")
        response["tweet_status"] = "Image fetch failed"
        return response

    # post tweet with image
    posted = tweet_image(img, caption=formatted)

    response["tweet_attempt"] = True
    response["quote"] = formatted

    if posted:
        log_telegram(f"Tweet posted successfully:\n\n{formatted}")
        response["tweet_status"] = "Posted"
    else:
        log_telegram("Quote bot: Image Tweet failed.")
        response["tweet_status"] = "Twitter failed"

    return response
