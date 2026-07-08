import discord
import random
import aiosqlite

from discord.ext import commands
from discord import app_commands

from database.database import (
    create_user,
    get_user
)


DATABASE = "database/users.db"


class Level(commands.Cog):

    def __init__(self, bot):

        self.bot = bot



    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return


        await create_user(
            message.author.id
        )


        xp = random.randint(
            5,
            15
        )


        async with aiosqlite.connect(
            DATABASE
        ) as db:


            await db.execute(
                """
                UPDATE users

                SET xp=xp+?

                WHERE user_id=?
                """,
                (
                    xp,
                    message.author.id
                )
            )


            await db.commit()



    @app_commands.command(
        name="rank",
        description="ดู Level และ XP"
    )
    async def rank(
        self,
        interaction:discord.Interaction
    ):


        await create_user(
            interaction.user.id
        )


        data = await get_user(
            interaction.user.id
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


        embed.add_field(
            name="Money",
            value=data[3]
        )


        await interaction.response.send_message(
            embed=embed
        )



async def setup(bot):

    await bot.add_cog(
        Level(bot)
    )