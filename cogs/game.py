from discord.ext import commands
from discord import app_commands
import discord
import random
import database
import time


class Game(commands.Cog):

    def __init__(self, bot):

        self.bot = bot
        database.setup()



    # โปรไฟล์
    @app_commands.command(
        name="profile",
        description="ดูข้อมูลตัวละคร"
    )
    async def profile(
        self,
        interaction: discord.Interaction
    ):

        uid = str(interaction.user.id)

        money, xp, level = database.get_user(uid)


        embed = discord.Embed(
            title=f"🎮 Profile ของ {interaction.user.name}"
        )

        embed.add_field(
            name="⭐ Level",
            value=level
        )

        embed.add_field(
            name="✨ EXP",
            value=xp
        )

        embed.add_field(
            name="💰 Money",
            value=money
        )


        await interaction.response.send_message(
            embed=embed
        )



    # Daily Reward
    @app_commands.command(
        name="daily",
        description="รับเงินรายวัน"
    )
    async def daily(
        self,
        interaction: discord.Interaction
    ):

        uid = str(interaction.user.id)


        reward = random.randint(
            100,
            500
        )


        # เพิ่ม EXP
        database.add_xp(
            uid,
            20
        )


        await interaction.response.send_message(
            f"🎁 ได้รับเงิน {reward} และ EXP 20"
        )



    # เพิ่ม EXP จากการพูด
    @commands.Cog.listener()
    async def on_message(
        self,
        message
    ):

        if message.author.bot:
            return


        database.add_xp(
            str(message.author.id),
            1
        )



async def setup(bot):

    await bot.add_cog(
        Game(bot)
    )