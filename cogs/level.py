import discord
from discord.ext import commands
import json
import os


FILE="data/levels.json"


if not os.path.exists(FILE):
    open(FILE,"w").write("{}")


class Level(commands.Cog):

    def __init__(self,bot):
        self.bot=bot


    @commands.Cog.listener()
    async def on_message(self,message):

        if message.author.bot:
            return

        data=json.load(open(FILE))

        uid=str(message.author.id)

        if uid not in data:
            data[uid]=0


        data[uid]+=10


        json.dump(
            data,
            open(FILE,"w"),
            indent=4
        )


async def setup(bot):
    await bot.add_cog(Level(bot))