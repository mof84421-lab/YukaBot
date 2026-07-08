import discord
from discord.ext import commands

import os
import asyncio
import logging


from config import config
from database.database import setup_database



logging.basicConfig(
    level=logging.INFO,
    filename="logs/bot.log",
    filemode="a",
    format="%(asctime)s | %(levelname)s | %(message)s"
)



intents = discord.Intents.all()



class YukaBot(commands.Bot):

    def __init__(self):

        super().__init__(
            command_prefix="!",
            intents=intents
        )


    async def setup_hook(self):

        await self.tree.sync()
print("Slash Commands Synced")


        for file in os.listdir("./cogs"):

            if file.endswith(".py"):

                try:

                    await self.load_extension(
                        f"cogs.{file[:-3]}"
                    )

                    print(
                        f"Loaded {file}"
                    )

                except Exception as e:

                    print(
                        f"Error {file}: {e}"
                    )



    async def on_ready(self):

        print(
            f"""
=========================
YukaBot Online

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



bot = YukaBot()



@bot.tree.command(
    name="ping",
    description="ตรวจสอบสถานะบอท"
)
async def ping(interaction):

    await interaction.response.send_message(
        f"Pong! {round(bot.latency*1000)}ms"
    )



async def main():

    async with bot:

        await bot.start(
            config.TOKEN
        )



if __name__ == "__main__":

    asyncio.run(main())