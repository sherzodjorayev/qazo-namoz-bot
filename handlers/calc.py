from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import aiosqlite, database

router = Router()

class CalcQazo(StatesGroup):
    waiting_for_years = State()


@router.message(F.text == "➕ Qazo hisoblash")
async def ask_years(m: types.Message, state: FSMContext):
    await m.answer("Necha yil qazo bormi? Faqat raqam yuboring.")
    await state.set_state(CalcQazo.waiting_for_years)


@router.message(CalcQazo.waiting_for_years)
async def save_year(m: types.Message, state: FSMContext):
    if not m.text.isdigit():
        return await m.answer("❗ Faqat raqam yuboring.")
    yil = int(m.text)
    plus = yil * 365
    async with aiosqlite.connect(database.DB) as db:
        await db.execute(
            "UPDATE qazo SET bomdod=bomdod+?, peshin=peshin+?, asr=asr+?, shom=shom+?, xufton=xufton+?, vitr=vitr+? WHERE user_id=?",
            (plus, plus, plus, plus, plus, plus, m.from_user.id)
        )
        await db.commit()
    await m.answer(f"✅ {yil} yillik qazo ({plus} tadan) qo‘shildi.")
    await state.clear()
