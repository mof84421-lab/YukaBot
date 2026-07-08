import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
print("TOKEN FOUND:", TOKEN is not None)
print("TOKEN LENGTH:", len(TOKEN) if TOKEN else 0)
intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


@bot.event
async def on_ready():

    print("===================")
    print(f"YukaBot Online : {bot.user}")
    print("===================")

    try:
        await bot.tree.sync()
        print("Slash Commands Ready")
    except Exception as e:
        print(e)


async def load_cogs():

    for file in os.listdir("./cogs"):

        if file.endswith(".py"):

            await bot.load_extension(
                f"cogs.{file[:-3]}"
            )


async def main():

    async with bot:

        await load_cogs()

        await bot.start(TOKEN)


asyncio.run(main())