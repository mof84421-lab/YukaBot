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
        "cogs.memory",
        "cogs.music",
        "cogs.moderation",
        "cogs.game"
    ]


    for cog in cogs:

        try:
            await bot.load_extension(cog)
            print("Loaded:", cog)

        except Exception as e:
            print(
                "Error:",
                cog,
                e
            )



@bot.event
async def on_ready():

    print("===================")
    print(
        "Yuka Online:",
        bot.user
    )
    print("===================")


    await bot.tree.sync()


    print(
        "Slash Commands Ready"
    )



async def main():

    async with bot:

        await load_cogs()

        await bot.start(
            TOKEN
        )



asyncio.run(main())