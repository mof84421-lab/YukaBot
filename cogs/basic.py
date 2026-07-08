import discord
from discord.ext import commands


class Basic(commands.Cog):

    def __init__(self,bot):
        self.bot = bot


    @discord.app_commands.command(
        name="ping",
        description="เช็กความเร็วบอท"
    )
    async def ping(self,interaction):

        await interaction.response.send_message(
            f"🏓 {round(self.bot.latency*1000)} ms"
        )


    @discord.app_commands.command(
        name="help",
        description="ดูคำสั่ง"
    )
    async def help(self,interaction):

        embed = discord.Embed(
            title="🤖 YukaBot",
            description="""
/ping
/help
/profile
"""
        )

        await interaction.response.send_message(
            embed=embed
        )


async def setup(bot):

    await bot.add_cog(Basic(bot))