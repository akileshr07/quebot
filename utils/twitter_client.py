import tweepy
import time
import os

def tweet(text):
    """
    Post tweet. Returns True on success, False otherwise.
    Simple retry and rudimentary rate-limit handling.
    """
    try:
        auth = tweepy.OAuth1UserHandler(
            os.getenv("X_API_KEY_TW"),
            os.getenv("X_API_SECRET"),
            os.getenv("X_ACCESS_TOKEN"),
            os.getenv("X_ACCESS_SECRET")
        )
        api = tweepy.API(auth)
    except Exception:
        return False

    for attempt in range(3):
        try:
            api.update_status(text)
            return True
        except Exception as e:
            err = str(e).lower()
            # simple rate-limit/backoff handling
            if "rate limit" in err or "429" in err:
                time.sleep(60)
            else:
                time.sleep(2)
    return False
