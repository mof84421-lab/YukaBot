import discord
from discord.ext import commands
import os
import asyncio

from dotenv import load_dotenv
from config import TOKEN


load_dotenv()


intents = discord.Intents.all()


class YukaBot(commands.Bot):

    def __init__(self):

        super().__init__(
            command_prefix="!",
            intents=intents
        )


    async def setup_hook(self):

        print("กำลังโหลดระบบ...")

        for file in os.listdir("./cogs"):

            if file.endswith(".py"):

                if file.startswith("_"):
                    continue

                try:

                    await self.load_extension(
                        f"cogs.{file[:-3]}"
                    )

                    print(
                        f"โหลด {file} สำเร็จ"
                    )

                except Exception as e:

                    print(
                        f"โหลด {file} ไม่สำเร็จ:",
                        e
                    )


        await self.tree.sync()

        print(
            "Slash Command พร้อมใช้งาน"
        )


bot = YukaBot()


@bot.event
async def on_ready():

    print(
        "===================="
    )

    print(
        f"Yuka ออนไลน์แล้ว: {bot.user}"
    )

    print(
        f"Server: {len(bot.guilds)}"
    )

    print(
        "===================="
    )


async def main():

    async with bot:

        await bot.start(
            TOKEN
        )


asyncio.run(main())