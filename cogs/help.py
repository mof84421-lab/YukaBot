import discord

from discord.ext import commands
from discord import app_commands



class Help(commands.Cog):

    def __init__(self,bot):

        self.bot = bot



    @app_commands.command(
        name="help",
        description="ดูคำสั่งทั้งหมด"
    )
    async def help(
        self,
        interaction:discord.Interaction
    ):


        embed = discord.Embed(

            title="🤖 YukaBot Commands",

            color=0x00ffff

        )


        embed.add_field(

            name="🛡 Moderation",

            value=
            """
/ban
/kick
/clear
/timeout
""",

            inline=False

        )


        embed.add_field(

            name="🎫 Ticket",

            value=
            """
/ticket
/close
""",

            inline=False

        )


        embed.add_field(

            name="💰 Economy",

            value=
            """
/balance
/daily
/pay
""",

            inline=False

        )


        embed.add_field(

            name="🤖 AI",

            value=
            """
/ask
""",

            inline=False

        )


        await interaction.response.send_message(
            embed=embed
        )



async def setup(bot):

    await bot.add_cog(
        Help(bot)
    )