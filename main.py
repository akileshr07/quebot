import datetime
from utils.quote_fetcher import fetch_quote
from utils.twitter_client import tweet
from utils.telegram_logger import log_telegram
from utils.format_quote import format_quote

def main():
    # Only run between 6 AM and 9 PM local time
    current_hour = datetime.datetime.now().hour
    if not (6 <= current_hour <= 21):
        return

    q = fetch_quote()
    if not q:
        log_telegram("Quote bot: Failed to fetch a new quote after retries.")
        return

    formatted = format_quote(q)
    if not formatted:
        log_telegram("Quote bot: Formatting failed.")
        return

    posted = tweet(formatted)
    if posted:
        log_telegram(f"Tweet posted successfully:\n\n{formatted}")
    else:
        log_telegram("Quote bot: Tweet failed after retries.")

if __name__ == "__main__":
    main()
