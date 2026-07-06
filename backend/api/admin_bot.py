# api/admin_bot.py
from fastapi import FastAPI, Request, Response
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import Update
import os
from datetime import datetime

app = FastAPI()

ADMIN_BOT_TOKEN = os.getenv("ADMIN_BOT_TOKEN")
ADMIN_USER_ID = int(os.getenv("ADMIN_USER_ID", "0"))

bot = Bot(token=ADMIN_BOT_TOKEN)
dp = Dispatcher()


@dp.message(lambda x: x.text == "/start")
async def cmd_start(message: types.Message):
    if message.from_user.id != ADMIN_USER_ID:
        await message.answer("⛔️ Доступ запрещён")
        return
    
    await message.answer(
        f"👋 Макс - админ-панель\n\n"
        f"📊 Статистика:\n"
        f"👥 Подписчиков: 1\n"
        f"📬 Уведомления активны"
    )


# Функция отправки уведомления
async def notify_maria(message_text: str, photo_url: str = None):
    try:
        if photo_url:
            await bot.send_photo(ADMIN_USER_ID, photo_url, caption=message_text)
        else:
            await bot.send_message(ADMIN_USER_ID, message_text)
    except Exception as e:
        print(f"Ошибка отправки: {e}")


# Webhook endpoint для админского бота
@app.post("/api/admin_bot")
async def webhook(request: Request):
    update = Update(**await request.json())
    await dp.feed_update(bot, update)
    return Response(status_code=200)


@app.get("/api/admin_bot")
async def health_check():
    return {"status": "ok"}