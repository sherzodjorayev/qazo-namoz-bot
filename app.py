from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
import asyncio
from handlers import start, qazo, calc, faq, admin, namoz
from handlers import help as help_router
from services.notifier import register_cron
from utils.set_bot_commands import set_default_commands
from config import BOT_TOKEN
from database import create_tables

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode="HTML")
)
dp = Dispatcher()

dp.include_router(start.router)
dp.include_router(qazo.router)
dp.include_router(calc.router)
dp.include_router(faq.router)
dp.include_router(namoz.router)
dp.include_router(help_router.router)
dp.include_router(admin.router)

async def main():
    await create_tables()
    await set_default_commands(bot)
    register_cron(bot)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
