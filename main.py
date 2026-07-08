import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


@bot.event
async def on_ready():
    print(f"ออนไลน์แล้ว: {bot.user}")

    try:
        synced = await bot.tree.sync()
        print(f"Sync {len(synced)} commands")
    except Exception as e:
        print(e)


async def load_extensions():

    folders = [
        "welcome",
        "moderation",
        "ticket",
        "level",
        "ai",
        "music",
        "help"
    ]

    for file in folders:
        await bot.load_extension(
            f"cogs.{file}"
        )


async def main():

    async with bot:
        await load_extensions()
        await bot.start(TOKEN)


import asyncio
asyncio.run(main())