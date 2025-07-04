# handlers/admin.py
from __future__ import annotations
import datetime as dt
from functools import wraps
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import aiosqlite, database
from config import ADMIN_IDS

router = Router()

# ───────────── Dekorator ─────────────
def admin_only(handler):
    @wraps(handler)
    async def wrapper(message: types.Message, **data):
        if message.from_user.id not in ADMIN_IDS:
            return await message.answer("🚫 Ruxsat yo‘q.")
        return await handler(message, **data)
    return wrapper

# ───────────── /users ─────────────
@router.message(Command("users"))
@admin_only
async def cmd_users(m: types.Message):
    async with aiosqlite.connect(database.DB) as db:
        cur = await db.execute("SELECT COUNT(*) FROM users")
        cnt = (await cur.fetchone())[0]
    await m.answer(f"👥 Foydalanuvchilar soni: <b>{cnt}</b>", parse_mode="HTML")

# ───────────── /stats ─────────────
@router.message(Command("stats"))
@admin_only
async def cmd_stats(m: types.Message):
    async with aiosqlite.connect(database.DB) as db:
        now = dt.datetime.utcnow()
        ranges = {
            "24 soat": now - dt.timedelta(days=1),
            "7 kun":   now - dt.timedelta(days=7),
            "30 kun":  now - dt.timedelta(days=30)
        }
        out = ["📊 <b>Ro‘yxatdan o‘tganlar</b>"]
        for title, mark in ranges.items():
            cur = await db.execute(
                "SELECT COUNT(*) FROM users WHERE registrated_time>=?",
                (mark.isoformat(),)
            )
            out.append(f"▪️ {title}: <b>{(await cur.fetchone())[0]}</b>")
    await m.answer("\n".join(out), parse_mode="HTML")

# ───────────── /qazo_stats ─────────────
@router.message(Command("qazo_stats"))
@admin_only
async def cmd_qazo_stats(m: types.Message):
    stats = await database.get_qazo_stats()
    txt = "🕌 <b>Umumiy qazo summasi</b>\n" + "\n".join(
        f"▪️ {k.capitalize()}: <b>{v}</b>" for k, v in stats.items()
    )
    await m.answer(txt, parse_mode="HTML")

# ───────────── Broadcast FSM ─────────────
class Broadcast(StatesGroup):
    waiting = State()

@router.message(Command("broadcast"))
@admin_only
async def bc_start(m: types.Message, state: FSMContext):
    await state.set_state(Broadcast.waiting)
    await m.answer("✉️ Xabar matnini yuboring (bekor: /cancel)")

@router.message(Broadcast.waiting, F.text.casefold() == "/cancel")
async def bc_cancel(m: types.Message, state: FSMContext):
    await state.clear()
    await m.answer("✅ Bekor qilindi.")

@router.message(Broadcast.waiting)
async def bc_send(m: types.Message, state: FSMContext, bot):
    txt = m.html_text
    await m.answer("⏳ Yuborilmoqda…")
    sent = fail = 0
    async with aiosqlite.connect(database.DB) as db:
        async with db.execute("SELECT user_id FROM users WHERE is_active=1") as cur:
            async for (uid,) in cur:
                try:
                    await bot.send_message(uid, txt, parse_mode="HTML")
                    sent += 1
                except Exception:
                    fail += 1
    await state.clear()
    await m.answer(
        f"📤 Yuborildi: <b>{sent}</b>\n❌ Xato: <b>{fail}</b>",
        parse_mode="HTML"
    )

# ───────────── FAQ qo‘shish FSM ─────────────
class AddFAQ(StatesGroup):
    q = State()
    a = State()

@router.message(Command("faq_add"))
@admin_only
async def faq_add_1(m: types.Message, state: FSMContext):
    await state.set_state(AddFAQ.q)
    await m.answer("📝 Savol matni:")

@router.message(AddFAQ.q)
async def faq_add_2(m: types.Message, state: FSMContext):
    await state.update_data(q=m.text)
    await state.set_state(AddFAQ.a)
    await m.answer("✍️ Javob matni:")

@router.message(AddFAQ.a)
async def faq_save(m: types.Message, state: FSMContext):
    data = await state.get_data()
    async with aiosqlite.connect(database.DB) as db:
        await db.execute(
            "INSERT INTO faq(question, answer) VALUES (?,?)",
            (data["q"], m.text)
        )
        await db.commit()
    await state.clear()
    await m.answer("✅ FAQ saqlandi.")

# ───────────── FAQ o‘chirish /faq_del <id> ─────────────
@router.message(Command("faq_del"))
@admin_only
async def faq_del(m: types.Message):
    args = m.text.split(maxsplit=1)
    if len(args) != 2 or not args[1].isdigit():
        return await m.answer("⚠️ Sintaksis: <code>/faq_del ID</code>", parse_mode="HTML")
    faq_id = int(args[1])
    async with aiosqlite.connect(database.DB) as db:
        cur = await db.execute("DELETE FROM faq WHERE id=?", (faq_id,))
        await db.commit()
    await m.answer("🗑 O‘chirildi." if cur.rowcount else "❓ ID topilmadi.")

# ───────────── Qazo RESET /reset <user_id> ─────────────
@router.message(Command("reset"))
@admin_only
async def reset_cmd(m: types.Message):
    args = m.text.split(maxsplit=1)
    if len(args) != 2 or not args[1].isdigit():
        return await m.answer("Sintaksis: /reset <code>user_id</code>", parse_mode="HTML")
    uid = int(args[1])
    await database.reset_qazo(uid)
    await m.answer("♻️ Qazo 0 ga tushirildi.")

# ───────────── SET QAZO /setqazo uid bomdod=3 xufton=1 … ─────────────
@router.message(Command("setqazo"))
@admin_only
async def set_qazo_cmd(m: types.Message):
    parts = m.text.split()
    if len(parts) < 3 or not parts[1].isdigit():
        return await m.answer(
            "Misol: <code>/setqazo 123456 bomdod=5 xufton=2</code>",
            parse_mode="HTML"
        )
    uid = int(parts[1])
    kv = {}
    for p in parts[2:]:
        if "=" in p:
            k, v = p.split("=", 1)
            if k in ("bomdod", "peshin", "asr", "shom", "xufton", "vitr") and v.isdigit():
                kv[k] = int(v)
    if not kv:
        return await m.answer("Hech qaysi to‘g‘ri namoz topilmadi.")
    await database.update_qazo(uid, **kv)
    await m.answer("✅ Yangilandi.")

# ───────────── USER DELETE /deluser <uid> ─────────────
@router.message(Command("deluser"))
@admin_only
async def del_user_cmd(m: types.Message):
    args = m.text.split(maxsplit=1)
    if len(args) != 2 or not args[1].isdigit():
        return await m.answer("Sintaksis: /deluser <code>user_id</code>", parse_mode="HTML")
    uid = int(args[1])
    await database.delete_user(uid)
    await m.answer("🗑 Foydalanuvchi o‘chirildi (agar mavjud bo‘lsa).")
