import os
import time
import requests
from bs4 import BeautifulSoup

# ===== SETTINGS =====
LAZADA_URL = "https://s.lazada.sg/s.TkVZb?c=w"

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

CHECK_EVERY = 5  # seconds


def send_telegram(message):
    if not BOT_TOKEN or not CHAT_ID:
        print("Telegram secrets are missing.")
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": message
        },
        timeout=15
    )


def check_lazada():
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Linux; Android 13) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0 Mobile Safari/537.36"
        )
    }

    response = requests.get(
        LAZADA_URL,
        headers=headers,
        timeout=15
    )

    soup = BeautifulSoup(response.text, "html.parser")

    page_text = soup.get_text(" ", strip=True).lower()

    buy_words = [
        "buy now",
        "add to cart"
    ]

    return any(word in page_text for word in buy_words)


print("PikaDrops Lazada monitor started!")

already_alerted = False

while True:
    try:
        available = check_lazada()

        if available and not already_alerted:
            print("BUY BUTTON FOUND!")

            send_telegram(
                "🚨 POKÉMON DROP DETECTED!\n\n"
                "Buy Now / Add to Cart appears available:\n"
                f"{LAZADA_URL}"
            )

            already_alerted = True

        elif not available:
            print("Not available yet...")
            already_alerted = False

    except Exception as e:
        print("Error:", e)

    time.sleep(CHECK_EVERY)
