from flask import Flask, request
import requests
import os
from openai import OpenAI

app = Flask(__name__)

LINE_TOKEN = os.environ.get("LINE_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """
20代男性。
短文。
少し煽る。
APEX好き。
「草」「いやそれな」を使う。
返信は1〜2文。
"""

@app.route("/", methods=["GET"])
def home():
    return "LINE bot is running"

@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.json

    for event in data.get("events", []):

        if event.get("type") == "message":

            if event["message"].get("type") == "text":

                message = event["message"]["text"]
                reply_token = event["replyToken"]

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "system",
                            "content": SYSTEM_PROMPT
                        },
                        {
                            "role": "user",
                            "content": message
                        }
                    ]
                )

                reply_text = response.choices[0].message.content

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
