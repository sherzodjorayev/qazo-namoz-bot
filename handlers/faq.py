from aiogram import Router, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

# ❓ Savollar tugmasi bosilganda tugmalar chiqadi
@router.message(F.text == "❓Savollar")
async def faq_button(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Qazo nima?", callback_data="faq:qazo")],
        [InlineKeyboardButton(text="Qazo namoz qanday o‘qiladi?", callback_data="faq:how")],
        [InlineKeyboardButton(text="Qazo qachon o‘qiladi?", callback_data="faq:when")],
    ])
    await message.answer("Quyidagi savollardan birini tanlang 👇", reply_markup=keyboard)

# Tugmalar bosilganda javob chiqadi
@router.callback_query(F.data.startswith("faq:"))
async def faq_callback(call: types.CallbackQuery):
    data = call.data.split(":")[1]
    if data == "qazo":
        text = "🕋 <b>Qazo</b> — vaqti o‘tib ketgan, ammo hali o‘qilmagan namozdir."
    elif data == "how":
        text = "📖 Qazo namozlari odatdagidek o‘qiladi. Faqat niyatda 'qazo' deb aytiladi."
    elif data == "when":
        text = "🕒 Qazo namozini har qanday vaqtda (makruh vaqtlar bundan mustasno) o‘qish mumkin."
    else:
        text = "❗ Nomaʼlum savol."

    await call.message.answer(text, parse_mode="HTML")
    await call.answer()  # loading tugadi
