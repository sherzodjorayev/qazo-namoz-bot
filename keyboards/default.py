from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📊 Qazolarim"),
            KeyboardButton(text="➕ Qazo hisoblash")
        ],
        [
            KeyboardButton(text="🕌 Namoz vaqti"),
            KeyboardButton(text="❓Savollar")
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Bo‘limni tanlang"
)
