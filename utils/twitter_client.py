import tweepy
import os
import time

def tweet(text):
    consumer_key = os.getenv("X_API_KEY_TW")
    consumer_secret = os.getenv("X_API_SECRET")
    access_token = os.getenv("X_ACCESS_TOKEN")
    access_secret = os.getenv("X_ACCESS_SECRET")

    # FULL VERBOSE AUTH CHECK
    try:
        auth = tweepy.OAuth1UserHandler(
            consumer_key,
            consumer_secret,
            access_token,
            access_secret
        )
        api = tweepy.API(auth)

        # Check credentials
        api.verify_credentials()
    except Exception as e:
        print("AUTH ERROR:", str(e))
        return False

    # Try posting
    for attempt in range(3):
        try:
            api.update_status(text)
            return True
        except Exception as e:
            print("POST ERROR:", str(e))
            if "429" in str(e) or "rate limit" in str(e).lower():
                time.sleep(60)
            else:
                time.sleep(2)
    return False
