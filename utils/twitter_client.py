import tweepy
import os
import time
import sys

def tweet(text):
    consumer_key = os.getenv("X_API_KEY_TW")
    consumer_secret = os.getenv("X_API_SECRET")
    access_token = os.getenv("X_ACCESS_TOKEN")
    access_secret = os.getenv("X_ACCESS_SECRET")

    print("TWITTER DEBUG: starting auth...", flush=True)

    # AUTH CHECK
    try:
        auth = tweepy.OAuth1UserHandler(
            consumer_key,
            consumer_secret,
            access_token,
            access_secret
        )
        api = tweepy.API(auth)

        print("TWITTER DEBUG: calling verify_credentials()", flush=True)
        api.verify_credentials()
        print("TWITTER DEBUG: credentials OK", flush=True)

    except Exception as e:
        print("AUTH ERROR:", str(e), flush=True)
        return False

    # POST TWEET
    for attempt in range(3):
        try:
            print(f"TWITTER DEBUG: posting attempt {attempt+1}", flush=True)
            api.update_status(text)
            print("TWITTER DEBUG: POST SUCCESS", flush=True)
            return True
        except Exception as e:
            print("POST ERROR:", str(e), flush=True)
            time.sleep(2)

    return False
