from discord.ext import commands
from discord import app_commands

from config import AI_NAME, PERSONALITY


class AI(commands.Cog):

    def __init__(self, bot):
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

        await interaction.response.defer()


        answer = f"""
🤖 {AI_NAME}

{PERSONALITY}

คำถาม:
{message}


Yuka กำลังพัฒนา AI Engine
สามารถเพิ่มโมเดล AI จริงได้ในอนาคต
"""


        await interaction.followup.send(answer)



async def setup(bot):

    await bot.add_cog(
        AI(bot)
    )