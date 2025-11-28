from flask import Flask
from main import main as run_bot

app = Flask(__name__)

@app.route("/")
def home():
    return "Quote Bot is Active!"

@app.route("/run")
def run():
    run_bot()
    return "Bot executed successfully."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
