import requests
import os

def log_telegram(msg):
    url = f"https://api.telegram.org/bot{os.getenv('BOT_TOKEN')}/sendMessage"
    data = {"chat_id": os.getenv("ADMIN_ID"), "text": msg}
    requests.post(url, data=data)
