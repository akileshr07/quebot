import tweepy
import os

def get_client():
    key = os.getenv("X_API_KEY_TW")
    secret = os.getenv("X_API_SECRET")
    token = os.getenv("X_ACCESS_TOKEN")
    token_secret = os.getenv("X_ACCESS_SECRET")

    auth = tweepy.OAuth1UserHandler(
        key,
        secret,
        token,
        token_secret
    )

    return tweepy.API(auth)

def test_twitter():
    """Return FULL error message instead of just FAILED."""

    try:
        client = get_client()

        # Try verifying credentials
        client.verify_credentials()
        return {"ok": True, "error": None}

    except Exception as e:
        return {
            "ok": False,
            "error": str(e),
            "type": type(e).__name__
        }

def tweet(text):
    try:
        client = get_client()
        client.update_status(text)
        return True
    except Exception as e:
        return False
