import discord
from discord.ext import commands
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


async def load_cogs():

    cogs = [
        "cogs.ai",
        "cogs.memory",
        "cogs.welcome",
        "cogs.verify",
        "cogs.moderation"
    ]

    for cog in cogs:
        await bot.load_extension(cog)
        print("Loaded:", cog)



@bot.event
async def on_ready():

    print(f"Yuka Online : {bot.user}")

    await bot.tree.sync()

    print("Slash Commands Ready")



async def main():

    async with bot:

        await load_cogs()

        await bot.start(TOKEN)



asyncio.run(main())