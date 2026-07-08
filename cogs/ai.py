import discord
from discord.ext import commands
from openai import OpenAI
import os


client=OpenAI(
    api_key=os.getenv(
        "OPENAI_API_KEY"
    )
)


class AI(commands.Cog):

    def __init__(self,bot):
        self.bot=bot


    @commands.command()
    async def ask(self,ctx,*,text):

        response=client.chat.completions.create(

            model="gpt-4.1-mini",

            messages=[
                {
                "role":"user",
                "content":text
                }
            ]
        )


        await ctx.send(
            response.choices[0].message.content
        )


async def setup(bot):
    await bot.add_cog(AI(bot))