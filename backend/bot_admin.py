# backend/bot_admin.py
from aiohttp_socks import ProxyConnector, ProxyType
from aiohttp import ClientSession

# Прокси
PROXY_HOST = '185.196.61.251'
PROXY_PORT = 1080

connector = ProxyConnector(
    proxy_type=ProxyType.SOCKS5,
    host=PROXY_HOST,
    port=PROXY_PORT,
)
session = ClientSession(connector=connector)

bot = Bot(token=ADMIN_BOT_TOKEN, session=session)

import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from datetime import datetime

# Токен админского бота (другой бот от @BotFather)
ADMIN_BOT_TOKEN = '8676468654:AAF90oFA7jhnK-9QMDiLZLn3HH-o7f9mjB8'
# ID Telegram аккаунта Марии (узнать через @userinfobot)
ADMIN_USER_ID = 1379473926  

logging.basicConfig(level=logging.INFO)
bot = Bot(token=ADMIN_BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    if message.from_user.id != ADMIN_USER_ID:
        return
    
    await message.answer(
        f"👋 Макс - админ-панель\n\n"
        f"📊 Статистика:\n"
        f"👥 Подписчиков: 1\n"
        f"📬 Уведомления активны"
    )


# Функция отправки уведомления Марии
async def notify_maria(message_text: str, photo_url: str = None):
    try:
        if photo_url:
            await bot.send_photo(ADMIN_USER_ID, photo_url, caption=message_text)
        else:
            await bot.send_message(ADMIN_USER_ID, message_text)
        logging.info(f"✅ Уведомление отправлено Марии")
    except Exception as e:
        logging.error(f"❌ Ошибка отправки: {e}")


# Пример: уведомление о новой заявке
async def notify_new_order(customer_name: str, work_title: str, customer_contact: str):
    await notify_maria(
        f"🔔 **НОВАЯ ЗАЯВКА!**\n\n"
        f"👤 Клиент: {customer_name}\n"
        f"🎨 Работа: {work_title}\n"
        f"📞 Контакты: {customer_contact}\n\n"
        f"⏰ {datetime.now().strftime('%d.%m.%Y %H:%M')}"
    )


# Пример: уведомление о новом сообщении с сайта
async def notify_website_message(name: str, email: str, message: str):
    await notify_maria(
        f"💬 **СООБЩЕНИЕ С САЙТА**\n\n"
        f"👤 Имя: {name}\n"
        f"✉️ Email: {email}\n"
        f"📝 Сообщение:\n{message}\n\n"
        f"⏰ {datetime.now().strftime('%d.%m.%Y %H:%M')}"
    )


async def main():
    logging.info("Запуск админского бота...")
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())