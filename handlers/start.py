# TODO: implement logic
from aiogram import Router, types
from aiogram.filters import Command
import aiosqlite, database, keyboards.default as kb

router = Router()

@router.message(Command("start"))
async def start(m: types.Message):
    async with aiosqlite.connect(database.DB) as db:
        await db.execute(
            "INSERT OR IGNORE INTO users(user_id,fullname,username) VALUES(?,?,?)",
            (m.from_user.id, m.from_user.full_name, m.from_user.username)
        )
        await db.execute("INSERT OR IGNORE INTO qazo(user_id) VALUES(?)", (m.from_user.id,))
        await db.commit()
    await m.answer(
        "Assalomu alaykum!\nQazo namozlaringizni hisoblashga yordam beruvchi botga xush kelibsiz.",
        reply_markup=kb.main_kb
    )
