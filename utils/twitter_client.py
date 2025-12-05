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
        client.create_tweet(text=text)
        return True
    except Exception:
        return False


# ---------- NEW IMAGE UPLOAD SUPPORT ----------
# Tweepy v2 client does NOT upload media directly
# We need the old v1.1 API for the media upload step.

def get_api_v1():
    auth = tweepy.OAuth1UserHandler(
        os.getenv("X_API_KEY_TW"),
        os.getenv("X_API_SECRET"),
        os.getenv("X_ACCESS_TOKEN"),
        os.getenv("X_ACCESS_SECRET"),
    )
    return tweepy.API(auth)


def tweet_image(image_path, caption=""):
    """
    Uploads image using Twitter API v1.1, then posts tweet using v2.
    Returns True/False.
    """
    try:
        api_v1 = get_api_v1()
        client_v2 = get_client()

        # upload image to v1
        media = api_v1.media_upload(image_path)
        media_id = media.media_id_string

        # create tweet with media in v2
        client_v2.create_tweet(text=caption, media_ids=[media_id])
        return True

    except Exception:
        return False
# ------------------------------------------------


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
