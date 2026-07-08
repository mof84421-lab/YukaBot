import discord
import aiosqlite

from discord.ext import commands
from discord import app_commands

from database.database import (
    create_user,
    get_user
)


DATABASE="database/users.db"



class Economy(commands.Cog):


    def __init__(self,bot):

        self.bot=bot



    @app_commands.command(
        name="balance",
        description="ดูเงิน"
    )
    async def balance(
        self,
        interaction:discord.Interaction
    ):


        await create_user(
            interaction.user.id
        )


        data=await get_user(
            interaction.user.id
        )


        await interaction.response.send_message(

            f"💰 เงินของคุณ: {data[3]}"

        )



    @app_commands.command(
        name="daily",
        description="รับเงินรายวัน"
    )
    async def daily(
        self,
        interaction:discord.Interaction
    ):


        await create_user(
            interaction.user.id
        )


        reward=500


        async with aiosqlite.connect(
            DATABASE
        ) as db:


            await db.execute(
                """
                UPDATE users

                SET money=money+?

                WHERE user_id=?
                """,
                (
                    reward,
                    interaction.user.id
                )
            )


            await db.commit()



        await interaction.response.send_message(

            f"🎁 ได้รับเงิน {reward}"

        )



    @app_commands.command(
        name="pay",
        description="โอนเงิน"
    )
    async def pay(
        self,
        interaction:discord.Interaction,
        member:discord.Member,
        amount:int
    ):


        if amount <= 0:

            await interaction.response.send_message(
                "❌ จำนวนเงินไม่ถูกต้อง",
                ephemeral=True
            )

            return



        await create_user(
            interaction.user.id
        )

        await create_user(
            member.id
        )


        sender = await get_user(
            interaction.user.id
        )


        if sender[3] < amount:

            await interaction.response.send_message(

                "❌ เงินไม่พอ",

                ephemeral=True

            )

            return



        async with aiosqlite.connect(
            DATABASE
        ) as db:


            await db.execute(
                """
                UPDATE users

                SET money=money-?

                WHERE user_id=?
                """,
                (
                    amount,
                    interaction.user.id
                )
            )


            await db.execute(
                """
                UPDATE users

                SET money=money+?

                WHERE user_id=?
                """,
                (
                    amount,
                    member.id
                )
            )


            await db.commit()



        await interaction.response.send_message(

            f"💸 โอน {amount} ให้ {member.mention}"

        )



async def setup(bot):

    await bot.add_cog(
        Economy(bot)
    )