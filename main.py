import datetime
from utils.quote_fetcher import fetch_quote
from utils.twitter_client import tweet
from utils.telegram_logger import log_telegram
from utils.format_quote import format_quote

def main():
    # Runs only between 6 AM and 9 PM
    current_hour = datetime.datetime.now().hour
    if not (6 <= current_hour <= 21):
        return

    # Get fresh non-duplicate quote
    quote = fetch_quote()
    if not quote:
        log_telegram("Failed to fetch a new quote.")
        return

    # Beautify for Twitter
    formatted = format_quote(quote)

    # Tweet with retry logic
    posted = tweet(formatted)

    if posted:
        log_telegram(f"Tweet posted:\n{formatted}")
    else:
        log_telegram("Tweet failed after retries.")

if __name__ == "__main__":
    main()
