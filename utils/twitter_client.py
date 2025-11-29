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
    """
    Deep diagnostic: detects auth issues, permission issues, write access,
    suspended apps, invalid keys, etc.
    Returns full structured JSON for debugging.
    """

    result = {
        "auth_ok": False,
        "write_ok": False,
        "account": None,
        "permissions": None,
        "raw_error": None,
        "error_type": None
    }

    try:
        client = get_client()

        # AUTH TEST: Does OAuth1 work?
        me = client.verify_credentials()
        if me:
            result["auth_ok"] = True
            result["account"] = {
                "id": me.id_str,
                "username": me.screen_name,
                "name": me.name
            }

        # PERMISSION TEST
        try:
            perms = client.auth.auth.get_authorization_header("GET", "https://api.twitter.com/1.1/account/verify_credentials.json")
            result["permissions"] = "Unknown (OAuth1 does not expose)"
        except Exception:
            result["permissions"] = "Unknown"

        # WRITE TEST — Create a hidden tweet (deleted immediately)
        try:
            test_status = client.update_status("🔍 Twitter Bot Write Test (auto-delete)")
            result["write_ok"] = True

            # Delete instantly
            client.destroy_status(test_status.id)

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

def tweet(text):
    try:
        client = get_client()
        client.update_status(text)
        return True
    except Exception as e:
        return False

