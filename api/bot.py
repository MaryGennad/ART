# api/bot.py
import os
import logging
from datetime import datetime
from fastapi import FastAPI, Request, Response
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Update, Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiohttp import ClientSession

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Переменные окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_BOT_TOKEN = os.getenv("ADMIN_BOT_TOKEN")
ADMIN_USER_ID = int(os.getenv("ADMIN_USER_ID", "0"))
API_URL = os.getenv("API_URL", "https://art-nine-kappa.vercel.app")

# Инициализация ботов
bot = Bot(token=BOT_TOKEN)
admin_bot = Bot(token=ADMIN_BOT_TOKEN) if ADMIN_BOT_TOKEN else None
dp = Dispatcher()


# ========== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ==========

def get_works_keyboard(works):
    """Создаёт клавиатуру со списком работ"""
    keyboard = []
    for work in works[:10]:
        keyboard.append([
            InlineKeyboardButton(
                text=f"🎨 {work['title']} - {work['price']} ₽",
                callback_data=f"work_{work['id']}"
            )
        ])
    keyboard.append([InlineKeyboardButton(text="🔄 Обновить", callback_data="refresh")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def notify_admin(message_text: str, photo_url: str = None):
    """Отправляет уведомление администратору (Марии)"""
    if not admin_bot or not ADMIN_USER_ID:
        logger.warning("Админский бот не настроен")
        return
    try:
        if photo_url:
            await admin_bot.send_photo(ADMIN_USER_ID, photo_url, caption=message_text)
        else:
            await admin_bot.send_message(ADMIN_USER_ID, message_text)
        logger.info(f"✅ Уведомление отправлено админу")
    except Exception as e:
        logger.error(f"❌ Ошибка отправки уведомления: {e}")


# ========== ОБРАБОТЧИКИ КОМАНД ==========

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        f"👋 Привет! Я Макс - помощник Марии.\n\n"
        f"🎨 Я могу показать работы художника и помочь с покупкой.\n\n"
        f"Выбери команду:\n"
        f"/works - Показать все работы\n"
        f"/about - О художнике\n"
        f"/contact - Связаться с Марией"
    )


@dp.message(Command("works"))
async def cmd_works(message: Message):
    try:
        async with ClientSession() as session:
            async with session.get(f"{API_URL}/api/works") as resp:
                works = await resp.json()
        
        if not works:
            await message.answer("😔 Пока нет доступных работ. Загляни позже!")
            return
        
        await message.answer(
            f"🎨 Доступно работ: {len(works)}\n\nВыбери картину:",
            reply_markup=get_works_keyboard(works)
        )
    except Exception as e:
        logger.error(f"Ошибка получения работ: {e}")
        await message.answer("😔 Произошла ошибка. Попробуй позже.")


@dp.message(Command("about"))
async def cmd_about(message: Message):
    try:
        async with ClientSession() as session:
            async with session.get(f"{API_URL}/api/about") as resp:
                about = await resp.json()
        
        await message.answer(
            f"👩‍ **{about['name']}**\n\n"
            f"✨ {about['tagline']}\n\n"
            f"{about['description']}",
            parse_mode="Markdown"
        )
    except Exception as e:
        logger.error(f"Ошибка получения about: {e}")
        await message.answer("😔 Произошла ошибка. Попробуй позже.")


@dp.message(Command("contact"))
async def cmd_contact(message: Message):
    await message.answer(
        f"📬 Связаться с Марией:\n\n"
        f"✉️ Email: maria@example.com\n"
        f"📱 Telegram: @maria_art\n"
        f"🛒 Авито: avito.ru/user/maria\n\n"
        f"Или напиши мне - я передам сообщение! 💌"
    )


# ========== ОБРАБОТЧИКИ CALLBACK ==========

@dp.callback_query(F.data.startswith('work_'))
async def process_work(callback: CallbackQuery):
    work_id = int(callback.data.split('_')[1])
    
    try:
        async with ClientSession() as session:
            async with session.get(f"{API_URL}/api/works/{work_id}") as resp:
                work = await resp.json()
        
        await bot.send_photo(
            chat_id=callback.from_user.id,
            photo=work['image_url'],
            caption=(
                f"🎨 **{work['title']}**\n\n"
                f"📐 {work['technique']}\n"
                f"💰 **Цена: {work['price']:,} ₽**\n\n"
                f"📝 {work.get('description', 'Описание отсутствует')}\n\n"
                f"✅ Доступна к покупке"
            ),
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="💌 Заказать", callback_data=f"order_{work_id}")],
                [InlineKeyboardButton(text="🔙 Назад к работам", callback_data="refresh")]
            ])
        )
    except Exception as e:
        logger.error(f"Ошибка обработки работы: {e}")
        await callback.message.answer("😔 Произошла ошибка.")
    
    await callback.answer()


@dp.callback_query(F.data.startswith('order_'))
async def process_order(callback: CallbackQuery):
    work_id = int(callback.data.split('_')[1])
    
    await bot.send_message(
        callback.from_user.id,
        f"✅ Отлично! Ты хочешь заказать работу #{work_id}.\n\n"
        f" Напиши свои контактные данные (имя и телефон/email), "
        f"и Мария свяжется с тобой!"
    )
    
    # Уведомляем админа
    await notify_admin(
        f"🔔 **НОВЫЙ ЗАКАЗ!**\n\n"
        f"👤 Клиент: {callback.from_user.full_name}\n"
        f" ID клиента: `{callback.from_user.id}`\n"
        f"🎨 Работа ID: {work_id}\n\n"
        f"⏰ {datetime.now().strftime('%d.%m.%Y %H:%M')}",
        parse_mode="Markdown"
    )
    
    await callback.answer()


@dp.callback_query(F.data == 'refresh')
async def refresh_works(callback: CallbackQuery):
    """Обновить список работ"""
    try:
        async with ClientSession() as session:
            async with session.get(f"{API_URL}/api/works") as resp:
                works = await resp.json()
        
        if not works:
            await callback.message.edit_text("😔 Пока нет доступных работ.")
            return
        
        await callback.message.edit_text(
            f"🎨 Доступно работ: {len(works)}\n\nВыбери картину:",
            reply_markup=get_works_keyboard(works)
        )
    except Exception as e:
        logger.error(f"Ошибка обновления: {e}")
    
    await callback.answer()


# ========== ОБРАБОТЧИК ВСЕХ СООБЩЕНИЙ ==========

@dp.message()
async def handle_message(message: Message):
    """Обрабатывает все остальные сообщения (заявки от клиентов)"""
    # Отправляем ответ клиенту
    await message.answer(
        f"📩 Спасибо! Мария получила твою заявку и скоро свяжется с тобой! 💕"
    )
    
    # Уведомляем админа
    await notify_admin(
        f"🔔 **НОВОЕ СООБЩЕНИЕ ОТ КЛИЕНТА!**\n\n"
        f"👤 Имя: {message.from_user.full_name}\n"
        f" ID: `{message.from_user.id}`\n"
        f"💬 Сообщение: {message.text}\n\n"
        f" {datetime.now().strftime('%d.%m.%Y %H:%M')}"
    )


# ========== WEBHOOK ENDPOINT ==========

@app.post("/api/bot")
async def webhook(request: Request):
    """Главный endpoint для webhook от Telegram"""
    try:
        update_data = await request.json()
        update = Update(**update_data)
        await dp.feed_update(bot, update)
        return Response(status_code=200)
    except Exception as e:
        logger.error(f"Ошибка webhook: {e}")
        return Response(status_code=500)


@app.get("/api/bot")
async def health_check():
    """Проверка работоспособности бота"""
    return {
        "status": "ok",
        "bot_username": (await bot.me()).username
    }