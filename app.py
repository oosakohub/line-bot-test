from flask import Flask, request
import requests
import os

app = Flask(__name__)

LINE_TOKEN = os.environ.get("LINE_TOKEN")

@app.route("/", methods=["GET"])
def home():
    return "LINE bot is running"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    for event in data.get("events", []):
        if event.get("type") == "message":
            message = event["message"].get("text", "")
            reply_token = event["replyToken"]

            reply_text = f"受信しました：{message}"

            headers = {
                "Authorization": f"Bearer {LINE_TOKEN}",
                "Content-Type": "application/json"
            }

            body = {
                "replyToken": reply_token,
                "messages": [
                    {
                        "type": "text",
                        "text": reply_text
                    }
                ]
            }

            requests.post(
                "https://api.line.me/v2/bot/message/reply",
                headers=headers,
                json=body
            )

    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
