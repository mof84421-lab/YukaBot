import discord
import random

from discord.ext import commands

from database.database import (
    create_user,
    get_user,
    add_xp
)


class Level(commands.Cog):

    def __init__(self, bot):

        self.bot = bot



    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return


        user_id = message.author.id


        await create_user(user_id)


        xp = random.randint(
            5,
            15
        )


        await add_xp(
            user_id,
            xp
        )


        data = await get_user(
            user_id
        )


        if data:

            level = data[2]

            current_xp = data[1]


            needed = level * 100


            if current_xp >= needed:


                async with __import__(
                    "aiosqlite"
                ).connect(
                    "database/users.db"
                ) as db:


                    await db.execute(
                    """
                    UPDATE users
                    SET level=level+1,
                    xp=0
                    WHERE user_id=?
                    """,
                    (user_id,)
                    )


                    await db.commit()



                await message.channel.send(

                    f"🎉 {message.author.mention} "
                    f"เลเวลเพิ่มเป็น {level+1}"

                )



    @commands.command(
        name="rank"
    )
    async def rank(
        self,
        ctx
    ):

        await create_user(
            ctx.author.id
        )


        data = await get_user(
            ctx.author.id
        )


        embed = discord.Embed(

            title="🏆 Rank",

            color=0x00ffff

        )


        embed.add_field(

            name="Level",

            value=data[2]

        )


        embed.add_field(

            name="XP",

            value=data[1]

        )


        await ctx.send(
            embed=embed
        )



async def setup(bot):

    await bot.add_cog(
        Level(bot)
    )