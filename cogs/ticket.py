import discord
from discord.ext import commands


class Ticket(commands.Cog):

    def __init__(self,bot):
        self.bot=bot


    @commands.command()
    async def ticket(self,ctx):

        guild=ctx.guild

        channel=await guild.create_text_channel(
            f"ticket-{ctx.author.name}"
        )

        await channel.send(
            f"{ctx.author.mention} เปิด Ticket แล้ว"
        )


async def setup(bot):
    await bot.add_cog(Ticket(bot))