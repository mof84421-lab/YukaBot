import discord
from discord.ext import commands

import os
import asyncio
import logging


from config import config
from database.database import setup_database


# =========================
# Logging System
# =========================

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    filename="logs/bot.log",
    filemode="a",
    format="%(asctime)s | %(levelname)s | %(message)s"
)


# =========================
# Discord Intents
# =========================

intents = discord.Intents.all()


# =========================
# YukaBot Class
# =========================

class YukaBot(commands.Bot):

    def __init__(self):

        super().__init__(
            command_prefix="!",
            intents=intents
        )

        # ป้องกัน Sync Command ซ้ำ
        self.synced = False


    async def setup_hook(self):

        # Database
        try:
            await setup_database()
            print("✅ Database Ready")

        except Exception as e:
            print(f"❌ Database Error: {e}")


        # Load Cogs

        if os.path.exists("./cogs"):

            for file in os.listdir("./cogs"):

                if file.endswith(".py"):

                    try:

                        await self.load_extension(
                            f"cogs.{file[:-3]}"
                        )

                        print(
                            f"✅ Loaded {file}"
                        )


                    except Exception as e:

                        print(
                            f"❌ Error loading {file}: {e}"
                        )


    async def on_ready(self):

        # Sync Slash Commands แค่ครั้งเดียว

        if not self.synced:

            try:

                synced = await self.tree.sync()

                print(
                    f"✅ Sync Commands สำเร็จ {len(synced)} คำสั่ง"
                )

                self.synced = True


            except Exception as e:

                print(
                    f"❌ Sync Error: {e}"
                )


        print(
f"""
=========================
🤖 YukaBot Online

Name:
{self.user}

ID:
{self.user.id}

Servers:
{len(self.guilds)}

=========================
"""
        )


        await self.change_presence(

            activity=discord.Game(
                name="/help | YukaBot"
            )

        )


# =========================
# Create Bot
# =========================

bot = YukaBot()



# =========================
# Test Slash Command
# =========================

@bot.tree.command(
    name="ping",
    description="ตรวจสอบสถานะบอท"
)
async def ping(
    interaction: discord.Interaction
):

    await interaction.response.send_message(
        f"🏓 Pong! {round(bot.latency * 1000)}ms"
    )



# =========================
# Error Handler
# =========================

@bot.tree.error
async def on_app_command_error(
    interaction: discord.Interaction,
    error
):

    if isinstance(
        error,
        discord.app_commands.MissingPermissions
    ):

        message = (
            "❌ คุณไม่มีสิทธิ์ใช้คำสั่งนี้"
        )


    elif isinstance(
        error,
        discord.app_commands.CommandOnCooldown
    ):

        message = (
            "⏳ กรุณารอสักครู่ก่อนใช้อีกครั้ง"
        )


    else:

        logging.error(
            f"Command Error: {error}"
        )

        message = (
            "❌ เกิดข้อผิดพลาดของระบบ"
        )


    try:

        if interaction.response.is_done():

            await interaction.followup.send(
                message,
                ephemeral=True
            )

        else:

            await interaction.response.send_message(
                message,
                ephemeral=True
            )


    except Exception as e:

        logging.error(
            f"Error Handler Failed: {e}"
        )



# =========================
# Run Bot
# =========================

async def main():

    # Delay ป้องกัน Render Restart แล้วยิง API ทันที
    await asyncio.sleep(5)


    async with bot:

        await bot.start(
            config.TOKEN
        )



if __name__ == "__main__":

    asyncio.run(main())