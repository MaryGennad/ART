import os
import requests
from dotenv import load_dotenv

load_dotenv()

ADMIN_BOT_TOKEN = os.getenv("ADMIN_BOT_TOKEN")
WEBHOOK_URL = os.getenv("VERCEL_URL", "https://art-nine-kappa.vercel.app") + "/api/admin_bot"

# Устанавливаем webhook для админского бота
url = f"https://api.telegram.org/bot{ADMIN_BOT_TOKEN}/setWebhook"
data = {
    "url": WEBHOOK_URL
}

response = requests.post(url, json=data)
print(response.json())