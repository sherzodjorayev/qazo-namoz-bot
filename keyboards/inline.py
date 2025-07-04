from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def qazo_edit_kb(_):
    buttons = []
    for namoz in ["bomdod", "peshin", "asr", "shom", "xufton", "vitr"]:
        row = [
            InlineKeyboardButton(text="➖", callback_data=f"dec:{namoz}"),
            InlineKeyboardButton(text=namoz.capitalize(), callback_data="ignore"),
            InlineKeyboardButton(text="➕", callback_data=f"inc:{namoz}")
        ]
        buttons.append(row)
    return InlineKeyboardMarkup(inline_keyboard=buttons)
