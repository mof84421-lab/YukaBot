import discord
from discord.ext import commands


class Moderation(commands.Cog):

    def __init__(self,bot):
        self.bot=bot


    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self,ctx,member:discord.Member):

        await member.kick()

        await ctx.send(
            f"เตะ {member}"
        )


    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self,ctx,amount:int):

        await ctx.channel.purge(
            limit=amount
        )


async def setup(bot):
    await bot.add_cog(
        Moderation(bot)
    )