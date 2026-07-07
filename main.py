import discord
from discord.ext import commands
import os
import asyncio

from config import TOKEN


intents = discord.Intents.default()
intents.message_content = True
intents.members = True


class YukaBot(commands.Bot):

    async def setup_hook(self):

        for file in os.listdir("./cogs"):

            if file.endswith(".py"):

                await self.load_extension(
                    f"cogs.{file[:-3]}"
                )

        await self.tree.sync()


bot = YukaBot(
    command_prefix="/",
    intents=intents
)


@bot.event
async def on_ready():

    print(
        f"✅ YukaBot Online : {bot.user}"
    )

    await bot.change_presence(
        activity=discord.Game(
            "Yuka AI Assistant 💙"
        )
    )


if TOKEN:
    bot.run(TOKEN)

else:
    print(
        "❌ ไม่พบ Token"
    )