import aiocron
from aiogram import Bot
from database import get_all_users, add_qazo
from datetime import datetime

bot: Bot = None  # global o'zgaruvchi

def register_cron(app_bot: Bot):
    global bot
    bot = app_bot

    aiocron.crontab("0 22 * * *")(nightly)  # 22:00 da ishga tushadi

async def nightly():
    users = await get_all_users()
    for user in users:
        await add_qazo(user["user_id"], datetime.now())  # misol uchun
        try:
            await bot.send_message(user["user_id"], "Bugungi qazo namozlaringiz qo‘shildi.")
        except:
            continue
