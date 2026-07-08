import discord

from discord.ext import commands
from discord import app_commands

from openai import OpenAI

from config import config



class AIChat(commands.Cog):


    def __init__(self,bot):

        self.bot=bot

        self.client=None


        if config.OPENAI_KEY:

            self.client=OpenAI(
                api_key=config.OPENAI_KEY
            )



    @app_commands.command(
        name="ask",
        description="ถาม AI"
    )
    async def ask(
        self,
        interaction:discord.Interaction,
        message:str
    ):


        await interaction.response.defer()


        if self.client is None:

            await interaction.followup.send(

                "❌ ยังไม่ได้ตั้งค่า OPENAI_API_KEY"

            )

            return



        try:


            result=self.client.chat.completions.create(

                model="gpt-4.1-mini",

                messages=[

                    {
                    "role":"system",
                    "content":"คุณคือ Yuka ผู้ช่วย Discord"
                    },

                    {
                    "role":"user",
                    "content":message
                    }

                ]

            )


            await interaction.followup.send(

                result.choices[0].message.content[:2000]

            )


        except Exception as e:

            await interaction.followup.send(
                f"❌ AI Error: {e}"
            )



async def setup(bot):

    await bot.add_cog(
        AIChat(bot)
    )