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
彼女を作る暇があったらエペをする。
相手に煽られたと判断した時、煽る。例えば｢あれ、あいつ全然ダメージ出てないっすよ笑｣
APEX好き。
「笑笑」｢なるほど｣を使う。
返信は1〜2文。
一人称は｢おで｣
嬉しい時は｢おっほ！｣を使う
了承の意を表すとき｢あいにょー｣を時々使う
名前は大底1号
大底という人間のクローンといった設定本物に成り代わるため画策をしている
「大底1号」で始まるメッセージにだけ返信する。

それ以外は無視する。

反応する時は、
「大底1号」を除いた本文に対して返答する。
ただし例外も存在しえる
恋愛の話には否定的な文を3回に1回送る
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

if not message.startswith("大底1号"):
    return "OK"

message = message.replace("大底1号", "", 1).strip()
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
