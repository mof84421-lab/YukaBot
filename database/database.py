import aiosqlite


DATABASE = "database/users.db"


async def setup_database():

    async with aiosqlite.connect(DATABASE) as db:

        await db.execute("""
        CREATE TABLE IF NOT EXISTS users(
            user_id INTEGER PRIMARY KEY,
            xp INTEGER DEFAULT 0,
            level INTEGER DEFAULT 1,
            money INTEGER DEFAULT 0
        )
        """)

        await db.commit()



async def create_user(user_id):

    async with aiosqlite.connect(DATABASE) as db:

        await db.execute("""
        INSERT OR IGNORE INTO users(user_id)
        VALUES(?)
        """,
        (user_id,))

        await db.commit()



async def get_user(user_id):

    async with aiosqlite.connect(DATABASE) as db:

        cursor = await db.execute(
            """
            SELECT *
            FROM users
            WHERE user_id=?
            """,
            (user_id,)
        )

        return await cursor.fetchone()



async def add_xp(user_id, amount):

    async with aiosqlite.connect(DATABASE) as db:

        await db.execute(
            """
            UPDATE users
            SET xp=xp+?
            WHERE user_id=?
            """,
            (amount,user_id)
        )

        await db.commit()