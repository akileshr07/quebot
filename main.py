import datetime
from utils.quote_fetcher import fetch_quote
from utils.twitter_client import tweet
from utils.telegram_logger import log_telegram

def main():
    hour = datetime.datetime.now().hour

    if not (6 <= hour <= 21):
        return

    quote = fetch_quote()

    if not quote:
        log_telegram("Failed to fetch a new quote.")
        return

    ok = tweet(quote)

    if ok:
        log_telegram(f"Tweet posted:\n{quote}")
    else:
        log_telegram("Tweet failed after retries.")

if __name__ == "__main__":
    main()
