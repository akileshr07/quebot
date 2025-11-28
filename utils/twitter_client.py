import tweepy
import time
import os

def tweet(text):
    auth = tweepy.OAuth1UserHandler(
        os.getenv("X_API_KEY_TW"),
        os.getenv("X_API_SECRET"),
        os.getenv("X_ACCESS_TOKEN"),
        os.getenv("X_ACCESS_SECRET")
    )
    api = tweepy.API(auth)

    for attempt in range(3):
        try:
            api.update_status(text)
            return True
        except tweepy.TweepError as e:
            if "rate limit" in str(e).lower():
                time.sleep(15)
            time.sleep(2)
    return False
