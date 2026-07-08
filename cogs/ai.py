from discord.ext import commands
from discord import app_commands


class AI(commands.Cog):

    def __init__(self,bot):
        self.bot = bot


    @app_commands.command(
        name="ask",
        description="ถาม Yuka AI"
    )
    async def ask(
        self,
        interaction,
        message:str
    ):

        await interaction.response.send_message(
            f"🤖 Yuka:\nคุณถามว่า {message}"
        )



async def setup(bot):

    await bot.add_cog(AI(bot))