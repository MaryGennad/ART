import os
import requests
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("VERCEL_URL", "https://art-nine-kappa.vercel.app") + "/api/bot"

# Устанавливаем webhook
url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook"
data = {
    "url": WEBHOOK_URL
}

response = requests.post(url, json=data)
print(response.json())