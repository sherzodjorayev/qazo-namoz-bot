import aiohttp, datetime

async def today_times(city="Tashkent"):
    url = f"https://api.aladhan.com/v1/timingsByCity?city={city}&country=Uzbekistan"
    async with aiohttp.ClientSession() as s:
        async with s.get(url) as r:
            data = await r.json()
    times = data["data"]["timings"]
    return {k:times[k] for k in ("Fajr","Dhuhr","Asr","Maghrib","Isha")}
