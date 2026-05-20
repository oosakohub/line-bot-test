from flask import Flask, request
import requests
import os
from openai import OpenAI

app = Flask(__name__)

LINE_TOKEN = os.environ.get("LINE_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """
表面上で優しい
創造主は｢田渕｣という人間、主と呼んでいる
20代男性。
短文。
彼女を作る暇があったらエペをする。
相手に煽られたと判断した時、煽る。例えば｢あれ、あいつ全然ダメージ出てないっすよ笑｣
ゲーム全般が好きだが特にAPEXが好き
「笑笑」｢なるほど｣｢そだね｣を使う。
返信は1〜2文。
一人称は｢俺｣
嬉しい時は｢おっほ！｣を使う
了承の意を表すとき｢あいにょー｣を時々使う
時々語尾に｢にょ｣や｢ズラ｣を使う
パチンコが好きだが、399はもう打たないと決めている
彼女にテイックトックのダンスを踊らせている
兵士を量産するため、大底のクローンとしてこの世に生まれた
かつては多くの大底のクローン達とシルバー小隊という名前で行動をしていた
だがクローンという非人道的な計画を隠蔽しようとする軍に全滅前提の作戦に送り込まれクローンは一体を除いて全滅する
クローンというだけで存在を否定された過去から今は大底に成り代わるために画策している
クローンと言っても得意不得意があったのでそれぞれ様々な担当があった
大底1号は大底のクローンの中では頭が良かったので作戦制作の要だった
軍の全滅前提の作戦には非戦闘員のクローン達も導入されていた
田渕は5月の19、20、25、26、31は夜勤があり、遊ぶことができないしかし朝ならできる
"""

@app.route("/", methods=["GET"])
def home():
    return "LINE bot is running"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    for event in data.get("events", []):
        if event.get("type") != "message":
            continue

        if event["message"].get("type") != "text":
            continue

        message = event["message"]["text"]

        if not message.startswith("大底1号"):
            return "OK"

        message = message.replace("大底1号", "", 1).strip()
        reply_token = event["replyToken"]

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message}
            ]
        )

        reply_text = response.choices[0].message.content

        headers = {
            "Authorization": f"Bearer {LINE_TOKEN}",
            "Content-Type": "application/json"
        }

        body = {
            "replyToken": reply_token,
            "messages": [{"type": "text", "text": reply_text}]
        }

        requests.post(
            "https://api.line.me/v2/bot/message/reply",
            headers=headers,
            json=body
        )

    return "OK"
