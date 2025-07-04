from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("help"))
async def help_handler(message: types.Message):
    await message.answer(
        "🤖 <b>Qazo namoz hisoblovchi bot</b> yordam:\n\n"
        "📊 <b>Qazolarim</b> — hozirgi qazo namozlaringiz sonini ko‘rish\n"
        "➕ <b>Qazo hisoblash</b> — yil bo‘yicha qazo hisoblash (masalan, 3 yil)\n"
        "🕌 <b>Namoz vaqti</b> — bugungi Toshkentdagi namoz vaqtlarini ko‘rish\n"
        "❓ <b>Savollar</b> — @Qazo_Hisoblovchi_uz_bot deb yozib, kerakli savollarni tanlang\n\n"
        "📩 Yordam yoki taklif uchun: @sherzod2388? (admin)"
        , parse_mode="HTML"
    )
