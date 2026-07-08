import discord
from discord.ext import commands
import asyncio
import os
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
        "cogs.memory"
    ]

    for cog in cogs:
        await bot.load_extension(cog)
        print("Loaded:", cog)



@bot.event
async def on_ready():

    print("================")
    print("Yuka Online:", bot.user)
    print("================")

    await bot.tree.sync()

    print("Slash Command Ready")



async def main():

    async with bot:

        await load_cogs()

        await bot.start(TOKEN)



asyncio.run(main())