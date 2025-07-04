from aiogram import Router, types
import aiohttp

router = Router()

@router.message(lambda msg: msg.text == "🕌 Namoz vaqti")  # tugmadagi matn bilan aynan bir xil
async def send_namoz_times(message: types.Message):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.aladhan.com/v1/timingsByCity?city=Tashkent&country=Uzbekistan&method=2") as resp:
            data = await resp.json()

    timings = data["data"]["timings"]

    text = (
        "🕌 <b>Bugungi namoz vaqtlari (Toshkent)</b>\n\n"
        f"📿 Bomdod: <b>{timings['Fajr']}</b>\n"
        f"🌞 Quyosh: <b>{timings['Sunrise']}</b>\n"
        f"🏙 Peshin: <b>{timings['Dhuhr']}</b>\n"
        f"🌇 Asr: <b>{timings['Asr']}</b>\n"
        f"🌆 Shom: <b>{timings['Maghrib']}</b>\n"
        f"🌃 Xufton: <b>{timings['Isha']}</b>"
    )

    await message.answer(text, parse_mode="HTML")
