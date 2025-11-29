import os
import tweepy

def get_client():
    return tweepy.Client(
        consumer_key=os.getenv("X_API_KEY_TW"),
        consumer_secret=os.getenv("X_API_SECRET"),
        access_token=os.getenv("X_ACCESS_TOKEN"),
        access_token_secret=os.getenv("X_ACCESS_SECRET"),
        return_type=dict
    )

def tweet(text):
    try:
        client = get_client()
        response = client.create_tweet(text=text)
        return True
    except Exception:
        return False
        
def test_connection():
    return {"status": "OK"}
               
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

        # try reading user info (auth check)
        try:
            me = client.get_me()
            if me and "data" in me:
                result["auth_ok"] = True
                user = me["data"]
                result["account"] = {
                    "id": user.get("id"),
                    "username": user.get("username"),
                    "name": user.get("name")
                }
        except Exception as e:
            result["raw_error"] = str(e)
            result["error_type"] = type(e).__name__
            return result

        # try writing a test tweet
        try:
            t = client.create_tweet(text="🔍 API v2 write-test (auto delete)")
            result["write_ok"] = True

            # delete immediately
            tid = t["data"]["id"]
            client.delete_tweet(tid)

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

