
import os
import time
import json
import feedparser
import openai
from telegram import Bot
from dotenv import load_dotenv

load_dotenv()

bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
openai.api_key = os.getenv("OPENAI_API_KEY")
chat_id = os.getenv("TELEGRAM_CHAT_ID")

with open("config.json") as f:
    config = json.load(f)

feeds = config["feeds"]
keywords = [k.lower() for k in config["keywords"]]
sent = set()

def contains_any(text):
    text = text.lower()
    return any(keyword in text for keyword in keywords)

def summarize(text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-preview",
            messages=[
                {"role": "system", "content": "Fornisci una sintesi in 5 righe con 3 takeaway."},
                {"role": "user", "content": text}
            ],
            max_tokens=500
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Errore nella sintesi: {e}"

def fetch_and_send():
    for url in feeds:
        d = feedparser.parse(url)
        for entry in d.entries:
            uid = entry.link
            if uid in sent:
                continue
            content = f"{entry.title}\n\n{entry.summary}"
            if contains_any(content):
                summary = summarize(content)
                message = f"📰 {entry.title}\n\n{summary}\n\n🔗 {entry.link}"
                bot.send_message(chat_id=chat_id, text=message)
                sent.add(uid)
    print("✅ Ciclo completato.")

if __name__ == "__main__":
    while True:
        fetch_and_send()
        time.sleep(7200)  # 2 ore
    