import discord
from discord.ext import commands


class Error(commands.Cog):

    def __init__(self,bot):
        self.bot=bot


    @commands.Cog.listener()
    async def on_command_error(
        self,
        ctx,
        error
    ):

        print(error)



async def setup(bot):

    await bot.add_cog(Error(bot))