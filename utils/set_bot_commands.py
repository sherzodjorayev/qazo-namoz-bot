# utils/set_bot_commands.py
from aiogram import Bot
from aiogram.types import BotCommand

async def set_default_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Botni qayta boshlash"),
        BotCommand(command="help", description="Yordam"),
        BotCommand(command="users", description="(Admin) Foydalanuvchilar soni"),
    ]
    await bot.set_my_commands(commands)
