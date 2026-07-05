import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiohttp import ClientSession
from aiohttp_socks import ProxyConnector, ProxyType

API_URL = "http://127.0.0.1:8000"

# Токен от @BotFather
BOT_TOKEN = "8936427601:AAHVReHJOJKNjt1krQJrLsOQEbVSh5dly18"

# Прокси для обхода блокировки Telegram
PROXY_HOST = '185.196.61.251'
PROXY_PORT = 1080
PROXY_TYPE = ProxyType.SOCKS5

logging.basicConfig(level=logging.INFO)

# Создаём сессию с прокси
connector = ProxyConnector(
    proxy_type=PROXY_TYPE,
    host=PROXY_HOST,
    port=PROXY_PORT,
)
session = ClientSession(connector=connector)

bot = Bot(token=BOT_TOKEN, session=session)
dp = Dispatcher()


# Клавиатура с работами
def get_works_keyboard(works):
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


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        f"👋 Привет! Я Макс - помощник Марии.\n\n"
        f"🎨 Я могу показать работы художника и помочь с покупкой.\n\n"
        f"Выбери команду:\n"
        f"/works - Показать все работы\n"
        f"/about - О художнике\n"
        f"/contact - Связаться с Марией"
    )


@dp.message(Command("works"))
async def cmd_works(message: types.Message):
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


@dp.callback_query(lambda c: c.data.startswith('work_'))
async def process_work(callback: types.CallbackQuery):
    work_id = int(callback.data.split('_')[1])
    
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
            [InlineKeyboardButton(text="🔙 Назад к работам", callback_data="back_to_works")]
        ])
    )
    await callback.answer()


@dp.callback_query(lambda c: c.data.startswith('order_'))
async def process_order(callback: types.CallbackQuery):
    work_id = int(callback.data.split('_')[1])
    await bot.send_message(
        callback.from_user.id,
        f"✅ Отлично! Ты хочешь заказать работу #{work_id}.\n\n"
        f"📩 Напиши свои контактные данные (имя и телефон/email), "
        f"и Мария свяжется с тобой!"
    )
    await callback.answer()


@dp.message()
async def handle_contact(message: types.Message):
    await message.answer(
        f"📩 Спасибо! Мария получила твою заявку и скоро свяжется с тобой! 💕"
    )


@dp.message(Command("about"))
async def cmd_about(message: types.Message):
    async with ClientSession() as session:
        async with session.get(f"{API_URL}/api/about") as resp:
            about = await resp.json()
    
    await message.answer(
        f"👩‍🎨 **{about['name']}**\n\n"
        f"✨ {about['tagline']}\n\n"
        f"{about['description']}"
    )


@dp.message(Command("contact"))
async def cmd_contact(message: types.Message):
    await message.answer(
        f"📬 Связаться с Марией:\n\n"
        f"✉️ Email: maria@example.com\n"
        f"📱 Telegram: @maria_art\n"
        f"🛒 Авито: avito.ru/user/maria\n\n"
        f"Или напиши мне - я передам сообщение! 💌"
    )


async def main():
    logging.info("Запуск клиентского бота...")
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())