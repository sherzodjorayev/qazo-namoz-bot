import aiosqlite

DB = "db.sqlite3"

# Jadval(lar)ni yaratish
async def create_tables():
    async with aiosqlite.connect(DB) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            fullname TEXT,
            username TEXT,
            registrated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active BOOLEAN DEFAULT 1
        )
        """)
        await db.execute("""
        CREATE TABLE IF NOT EXISTS qazo (
            user_id INTEGER PRIMARY KEY,
            bomdod INTEGER DEFAULT 0,
            peshin INTEGER DEFAULT 0,
            asr INTEGER DEFAULT 0,
            shom INTEGER DEFAULT 0,
            xufton INTEGER DEFAULT 0,
            vitr INTEGER DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
        """)
        await db.commit()

# Foydalanuvchini qo‘shish
async def add_user(user_id: int, fullname: str, username: str):
    async with aiosqlite.connect(DB) as db:
        await db.execute("""
        INSERT OR IGNORE INTO users (user_id, fullname, username)
        VALUES (?, ?, ?)
        """, (user_id, fullname, username))
        await db.execute("""
        INSERT OR IGNORE INTO qazo (user_id) VALUES (?)
        """, (user_id,))
        await db.commit()

# Barcha foydalanuvchilar ro‘yxati
async def get_all_users():
    users = []
    async with aiosqlite.connect(DB) as db:
        async with db.execute("SELECT user_id FROM users") as cursor:
            async for row in cursor:
                users.append({"user_id": row[0]})
    return users

# Foydalanuvchiga qazo qo‘shish
async def add_qazo(user_id: int, namoz: str):
    async with aiosqlite.connect(DB) as db:
        await db.execute(f"""
        UPDATE qazo SET {namoz} = {namoz} + 1 WHERE user_id = ?
        """, (user_id,))
        await db.commit()

# Bitta foydalanuvchining qazo statistikasi
async def get_qazo(user_id: int):
    async with aiosqlite.connect(DB) as db:
        async with db.execute("""
        SELECT bomdod, peshin, asr, shom, xufton, vitr FROM qazo WHERE user_id = ?
        """, (user_id,)) as cursor:
            row = await cursor.fetchone()
            if row:
                return {
                    "bomdod": row[0], "peshin": row[1], "asr": row[2],
                    "shom": row[3], "xufton": row[4], "vitr": row[5],
                }
            return None

# Umumiy qazo statistikasi (admin uchun)
async def get_qazo_stats():
    async with aiosqlite.connect(DB) as db:
        async with db.execute("""
        SELECT 
            SUM(bomdod), 
            SUM(peshin), 
            SUM(asr), 
            SUM(shom), 
            SUM(xufton), 
            SUM(vitr)
        FROM qazo
        """) as cursor:
            row = await cursor.fetchone()
            if row:
                return {
                    "bomdod": row[0] or 0,
                    "peshin": row[1] or 0,
                    "asr": row[2] or 0,
                    "shom": row[3] or 0,
                    "xufton": row[4] or 0,
                    "vitr": row[5] or 0,
                }
            return None
