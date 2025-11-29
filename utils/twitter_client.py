import tweepy
import os

def get_client():
    return tweepy.Client(
        consumer_key=os.getenv("X_API_KEY_TW"),
        consumer_secret=os.getenv("X_API_SECRET"),
        access_token=os.getenv("X_ACCESS_TOKEN"),
        access_token_secret=os.getenv("X_ACCESS_SECRET")
    )

def test_twitter():
    try:
        client = get_client()
        r = client.get_me()
        return {"ok": True, "me": r.data}
    except Exception as e:
        return {"ok": False, "error": str(e), "type": type(e).__name__}

def tweet(text):
    try:
        client = get_client()
        client.create_tweet(text=text)
        return True
    except Exception as e:
        return {"error": str(e), "type": type(e).__name__}
