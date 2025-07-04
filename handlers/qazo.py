from aiogram import Router, types, F
import aiosqlite, database, keyboards.inline as ikb

router = Router()
NAMOZLAR = ("bomdod", "peshin", "asr", "shom", "xufton", "vitr")


@router.message(F.text == "📊 Qazolarim")
async def show_qazo(m: types.Message):
    async with aiosqlite.connect(database.DB) as db:
        cursor = await db.execute(
            "SELECT bomdod,peshin,asr,shom,xufton,vitr FROM qazo WHERE user_id=?",
            (m.from_user.id,)
        )
        row = await cursor.fetchone()
        await cursor.close()

    if not row:
        return await m.answer("Maʼlumot topilmadi.")

    txt = "\n".join([f"• {n.capitalize()}: <b>{v}</b>" for n, v in zip(NAMOZLAR, row)])
    await m.answer(f"🕌 <b>Qazo namozlaringiz</b>\n{txt}",
                   reply_markup=ikb.qazo_edit_kb("all"), parse_mode="HTML")


@router.callback_query(F.data.startswith(("inc", "dec")))
async def inc_dec(call: types.CallbackQuery):
    op, namoz = call.data.split(":")
    if namoz not in NAMOZLAR:
        return await call.answer("Xato.")

    col = f"{namoz}"
    async with aiosqlite.connect(database.DB) as db:
        if op == "inc":
            await db.execute(f"UPDATE qazo SET {col}={col}+1 WHERE user_id=?", (call.from_user.id,))
        else:
            await db.execute(f"UPDATE qazo SET {col}=MAX({col}-1, 0) WHERE user_id=?", (call.from_user.id,))
        await db.commit()

    await call.answer(f"{namoz.capitalize()} yangilandi!")

    # Yangilangan sonni chiqarish
    await show_qazo_from_callback(call)


async def show_qazo_from_callback(call: types.CallbackQuery):
    async with aiosqlite.connect(database.DB) as db:
        cursor = await db.execute(
            "SELECT bomdod,peshin,asr,shom,xufton,vitr FROM qazo WHERE user_id=?",
            (call.from_user.id,)
        )
        row = await cursor.fetchone()
        await cursor.close()

    if not row:
        return await call.message.answer("Maʼlumot topilmadi.")

    txt = "\n".join([f"• {n.capitalize()}: <b>{v}</b>" for n, v in zip(NAMOZLAR, row)])
    await call.message.edit_text(f"🕌 <b>Qazo namozlaringiz</b>\n{txt}",
                                 reply_markup=ikb.qazo_edit_kb("all"), parse_mode="HTML")
