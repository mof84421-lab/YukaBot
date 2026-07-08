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


    async def setup_hook(self):

        # Database

        try:

            await setup_database()

            print(
                "✅ Database Ready"
            )

        except Exception as e:

            print(
                f"❌ Database Error: {e}"
            )


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


        # เปลี่ยนสถานะครั้งเดียว

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
# Test Command
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

    logging.error(
        f"Command Error: {error}"
    )


    try:

        if interaction.response.is_done():

            await interaction.followup.send(
                "❌ เกิดข้อผิดพลาด",
                ephemeral=True
            )

        else:

            await interaction.response.send_message(
                "❌ เกิดข้อผิดพลาด",
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

    # กัน Render Restart แล้วยิงทันที

    await asyncio.sleep(10)


    async with bot:

        await bot.start(
            config.TOKEN
        )



if __name__ == "__main__":

    asyncio.run(main())