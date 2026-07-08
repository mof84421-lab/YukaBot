import discord
from discord.ext import commands
from discord import app_commands

from openai import OpenAI

from config import config



class AIChat(commands.Cog):

    def __init__(self, bot):

        self.bot = bot


        if config.OPENAI_KEY:

            self.client = OpenAI(
                api_key=config.OPENAI_KEY
            )

        else:

            self.client = None



    @app_commands.command(
        name="ask",
        description="ถาม AI"
    )
    async def ask(

        self,
        interaction: discord.Interaction,

        message:str

    ):


        await interaction.response.defer()



        if self.client is None:

            await interaction.followup.send(
                "❌ ยังไม่ได้ใส่ OPENAI_API_KEY"
            )

            return



        try:

            response = self.client.chat.completions.create(

                model="gpt-4.1-mini",

                messages=[

                    {
                        "role":"system",
                        "content":
                        "คุณคือ Yuka AI ผู้ช่วยใน Discord"
                    },

                    {
                        "role":"user",
                        "content":message
                    }

                ]

            )


            answer = response.choices[0].message.content



            await interaction.followup.send(
                answer[:2000]
            )


        except Exception as e:

            await interaction.followup.send(
                f"เกิดข้อผิดพลาด: {e}"
            )



async def setup(bot):

    await bot.add_cog(
        AIChat(bot)
    )