import discord

from discord.ext import commands
from discord import app_commands

from music.player import MusicPlayer



class Music(commands.Cog):


    def __init__(self, bot):

        self.bot = bot

        self.player = MusicPlayer(
            bot
        )



    @app_commands.command(

        name="join",

        description="ให้บอทเข้าห้องเสียง"

    )
    async def join(

        self,

        interaction:discord.Interaction

    ):


        if interaction.user.voice:


            await interaction.user.voice.channel.connect()


            await interaction.response.send_message(

                "🎵 เข้าห้องเสียงแล้ว"

            )


        else:


            await interaction.response.send_message(

                "❌ คุณต้องอยู่ในห้องเสียงก่อน",

                ephemeral=True

            )



    @app_commands.command(

        name="leave",

        description="ให้บอทออกจากห้องเสียง"

    )
    async def leave(

        self,

        interaction:discord.Interaction

    ):


        await self.player.stop(

            interaction.guild

        )


        await interaction.response.send_message(

            "👋 ออกจากห้องเสียงแล้ว"

        )



async def setup(bot):

    await bot.add_cog(

        Music(bot)

    )