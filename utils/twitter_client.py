import tweepy
import os

def get_client_v2():
    return tweepy.Client(
        consumer_key=os.getenv("X_API_KEY_TW"),
        consumer_secret=os.getenv("X_API_SECRET"),
        access_token=os.getenv("X_ACCESS_TOKEN"),
        access_token_secret=os.getenv("X_ACCESS_SECRET")
    )

def tweet(text):
    try:
        client = get_client_v2()
        client.create_tweet(text=text)
        return True
    except Exception as e:
        print("ERROR:", e)
        return False
