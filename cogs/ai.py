import discord
from discord.ext import commands
from openai import OpenAI
import os
import json


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


class YukaAI(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @discord.app_commands.command(
        name="ask",
        description="ถาม Yuka AI"
    )
    async def ask(
        self,
        interaction: discord.Interaction,
        question: str
    ):

        await interaction.response.defer()


        user = interaction.user.name


        prompt = f"""
คุณคือ Yuka AI
เป็นผู้ช่วยใน Discord

บุคลิก:
- เป็นมิตร
- สุภาพ
- ตอบภาษาไทย
- ช่วยเหลือสมาชิก

ผู้ใช้ชื่อ {user}

คำถาม:
{question}
"""


        try:

            result = client.chat.completions.create(

                model="gpt-4o-mini",

                messages=[
                    {
                        "role":"system",
                        "content":prompt
                    }
                ]

            )


            answer = result.choices[0].message.content


            await interaction.followup.send(
                f"🤖 **Yuka:**\n{answer}"
            )


        except Exception as e:

            await interaction.followup.send(
                f"❌ Error:\n{e}"
            )



async def setup(bot):

    await bot.add_cog(YukaAI(bot))