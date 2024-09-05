from aiogram import Bot, Dispatcher, types
from const import BOT_TOKEN

bot = Bot(BOT_TOKEN)
dp = Dispatcher()


async def start_bot():
    await dp.start_polling(bot, polling_timeout=30000)
