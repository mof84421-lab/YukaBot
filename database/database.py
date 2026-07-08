import aiosqlite
import os


DATABASE = "database/users.db"



async def setup_database():

    # สร้างโฟลเดอร์ database ถ้ายังไม่มี
    os.makedirs(
        "database",
        exist_ok=True
    )


    async with aiosqlite.connect(DATABASE) as db:

        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS users(

                user_id INTEGER PRIMARY KEY,

                xp INTEGER DEFAULT 0,

                level INTEGER DEFAULT 1,

                money INTEGER DEFAULT 0

            )
            """
        )


        await db.commit()



async def create_user(user_id):

    async with aiosqlite.connect(DATABASE) as db:

        await db.execute(
            """
            INSERT OR IGNORE INTO users
            (
                user_id,
                xp,
                level,
                money
            )

            VALUES
            (
                ?,
                0,
                1,
                0
            )
            """,
            (user_id,)
        )


        await db.commit()



async def get_user(user_id):

    async with aiosqlite.connect(DATABASE) as db:

        cursor = await db.execute(
            """
            SELECT
                user_id,
                xp,
                level,
                money

            FROM users

            WHERE user_id=?
            """,
            (user_id,)
        )


        data = await cursor.fetchone()


        return data



async def add_xp(user_id, amount):

    await create_user(user_id)


    async with aiosqlite.connect(DATABASE) as db:

        await db.execute(
            """
            UPDATE users

            SET xp = xp + ?

            WHERE user_id=?
            """,
            (
                amount,
                user_id
            )
        )


        await db.commit()



async def add_money(user_id, amount):

    await create_user(user_id)


    async with aiosqlite.connect(DATABASE) as db:

        await db.execute(
            """
            UPDATE users

            SET money = money + ?

            WHERE user_id=?
            """,
            (
                amount,
                user_id
            )
        )


        await db.commit()



async def remove_money(user_id, amount):

    await create_user(user_id)


    async with aiosqlite.connect(DATABASE) as db:

        await db.execute(
            """
            UPDATE users

            SET money = money - ?

            WHERE user_id=?
            """,
            (
                amount,
                user_id
            )
        )


        await db.commit()



async def set_level(user_id, level):

    await create_user(user_id)


    async with aiosqlite.connect(DATABASE) as db:

        await db.execute(
            """
            UPDATE users

            SET level=?

            WHERE user_id=?
            """,
            (
                level,
                user_id
            )
        )


        await db.commit()



async def reset_xp(user_id):

    async with aiosqlite.connect(DATABASE) as db:

        await db.execute(
            """
            UPDATE users

            SET xp=0

            WHERE user_id=?
            """,
            (user_id,)
        )


        await db.commit()