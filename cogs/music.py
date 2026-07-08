import discord
from discord.ext import commands


class Music(commands.Cog):

    def __init__(self,bot):
        self.bot=bot


    @commands.command()
    async def join(self,ctx):

        if ctx.author.voice:

            await ctx.author.voice.channel.connect()


async def setup(bot):
    await bot.add_cog(
        Music(bot)
    )