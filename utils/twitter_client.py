import tweepy
import os

def get_v1_client():
    """v1.1 client for posting tweets (FREE)."""
    auth = tweepy.OAuth1UserHandler(
        os.getenv("X_API_KEY_TW"),
        os.getenv("X_API_SECRET"),
        os.getenv("X_ACCESS_TOKEN"),
        os.getenv("X_ACCESS_SECRET")
    )
    return tweepy.API(auth)

def get_v2_client():
    """v2 client for reading and account info (FREE)."""
    return tweepy.Client(
        consumer_key=os.getenv("X_API_KEY_TW"),
        consumer_secret=os.getenv("X_API_SECRET"),
        access_token=os.getenv("X_ACCESS_TOKEN"),
        access_token_secret=os.getenv("X_ACCESS_SECRET")
    )

def test_connection():
    result = {
        "auth_ok": False,
        "write_ok": False,
        "account": None,
        "error": None
    }

    try:
        api = get_v1_client()
        me = api.verify_credentials()

        if me:
            result["auth_ok"] = True
            result["account"] = {
                "id": me.id_str,
                "username": me.screen_name,
                "name": me.name
            }

        # Write test
        try:
            status = api.update_status("🔍 Tweet test (auto delete)")
            api.destroy_status(status.id)
            result["write_ok"] = True
        except Exception as e:
            result["error"] = str(e)

    except Exception as e:
        result["error"] = str(e)

    return result


def post_tweet(text):
    """POST tweet using v1.1 (works in free plan)."""
    try:
        api = get_v1_client()
        api.update_status(text)
        return True
    except Exception:
        return False
