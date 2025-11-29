import os
import tweepy

def get_client():
    return tweepy.Client(
        consumer_key=os.getenv("X_API_KEY_TW"),
        consumer_secret=os.getenv("X_API_SECRET"),
        access_token=os.getenv("X_ACCESS_TOKEN"),
        access_token_secret=os.getenv("X_ACCESS_SECRET")
    )

def tweet(text):
    try:
        client = get_client()
        response = client.create_tweet(text=text)
        return {
            "ok": True,
            "tweet_id": response.data["id"],
            "text": text
        }
    except Exception as e:
        return {
            "ok": False,
            "error": str(e),
            "error_type": type(e).__name__
        }

def test_twitter():
    result = {
        "auth_ok": False,
        "write_ok": False,
        "account": None,
        "raw_error": None,
        "error_type": None
    }

    try:
        client = get_client()

        # Auth Test — Get own account info (v2)
        try:
            me = client.get_me()
            if me.data:
                result["auth_ok"] = True
                result["account"] = {
                    "id": me.data.id,
                    "name": me.data.name,
                    "username": me.data.username
                }
        except Exception as e:
            result["raw_error"] = str(e)
            result["error_type"] = type(e).__name__
            return result

        # Write Test — Post then delete tweet
        try:
            tw = client.create_tweet(text="🔍 Twitter API v2 Test (auto-delete)")
            result["write_ok"] = True
            client.delete_tweet(tw.data["id"])
        except Exception as e:
            result["write_ok"] = False
            result["raw_error"] = str(e)
            result["error_type"] = type(e).__name__
            return result

        return result

    except Exception as e:
        result["raw_error"] = str(e)
        result["error_type"] = type(e).__name__
        return result
