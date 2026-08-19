import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiohttp import web

# ====================================================================
# НАСТРОЙКИ (Всё уже вписано!)
# ====================================================================
BOT_TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = 732059307

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ====================================================================
# КЛАВИАТУРЫ
# ====================================================================
main_user_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="💰 Донат в игры")],
        [KeyboardButton(text="💎 Покупка крипты")],
    ],
    resize_keyboard=True
)

# ====================================================================
# ХЕНДЛЕРЫ БОТА
# ====================================================================

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        f"👋 **Привет, {message.from_user.first_name}!**\n\n"
        f"Выберите, по какому вопросу вы хотите обратиться:",
        reply_markup=main_user_kb,
        parse_mode="Markdown"
    )

@dp.message(F.text == "💰 Донат в игры")
async def handle_game_donate(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username or "Не указан"

    admin_notify_text = (
        f"🔔 **НОВЫЙ ЗАПРОС - ДОНАТ В ИГРЫ!**\n\n"
        f"👤 Пользователь: @{username} (ID: `{user_id}`)\n"
        f"❓ Вопрос: **Донат в игры**"
    )
    
    reply_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✉️ Написать пользователю", url=f"tg://user?id={user_id}")]
    ])

    await bot.send_message(ADMIN_ID, admin_notify_text, reply_markup=reply_kb, parse_mode="Markdown")
    
    await message.answer(
        f"✅ Отлично! Я передал ваш запрос по **донату в игры** администратору.\n"
        f"Он скоро свяжется с вами для уточнения деталей!"
    )

@dp.message(F.text == "💎 Покупка крипты")
async def handle_crypto_buy(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username or "Не указан"

    admin_notify_text = (
        f"🔔 **НОВЫЙ ЗАПРОС - ПОКУПКА КРИПТЫ!**\n\n"
        f"👤 Пользователь: @{username} (ID: `{user_id}`)\n"
        f"❓ Вопрос: **Покупка крипты**"
    )
    
    reply_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✉️ Написать пользователю", url=f"tg://user?id={user_id}")]
    ])

    await bot.send_message(ADMIN_ID, admin_notify_text, reply_markup=reply_kb, parse_mode="Markdown")
    
    await message.answer(
        f"✅ Отлично! Я передал ваш запрос по **покупке крипты** администратору.\n"
        f"Он скоро свяжется с вами для уточнения деталей!"
    )

# ====================================================================
# ЗАГЛУШКА ВЕБ-СЕРВЕРА ДЛЯ СЕРВЕРА RENDER (ЧТОБЫ РАБОТАЛО БЕСПЛАТНО!)
# ====================================================================
async def web_handle(request):
    return web.Response(text="Bot is alive and running!")

# ====================================================================
# ЗАПУСК ВСЕГО ВМЕСТЕ
# ====================================================================
async def main():
    # Запуск микро-веб сервера на порту Render
    web_app = web.Application()
    web_app.router.add_get('/', web_handle)
    runner = web.AppRunner(web_app)
    await runner.setup()
    
    # Render сам выдаёт порт в переменную окружения PORT, если её нет — ставим 8000
    port = int(os.environ.get("PORT", 8000))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"🚀 Веб-сервер заглушки запущен на порту {port}")

    # Запуск прослушивания Телеграм-бота
    print("🚀 Бот успешно запущен и слушает сообщения!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())