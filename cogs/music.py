import discord

from discord.ext import commands
from discord import app_commands

from music.queue import MusicQueue
from music.player import MusicPlayer



class Music(commands.Cog):


    def __init__(self, bot):

        self.bot = bot

        self.queue = MusicQueue()

        self.player = MusicPlayer(
            bot,
            self.queue
        )



    @app_commands.command(

        name="join",

        description="เข้าห้องเสียง"

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
                "❌ คุณต้องอยู่ในห้องเสียงก่อน"
            )



    @app_commands.command(

        name="stop",

        description="หยุดเพลง"

    )
    async def stop(

        self,
        interaction:discord.Interaction

    ):


        voice = interaction.guild.voice_client


        if voice:

            await voice.disconnect()


            await interaction.response.send_message(
                "⏹ หยุดเพลงแล้ว"
            )


        else:

            await interaction.response.send_message(
                "ไม่ได้อยู่ในห้องเสียง"
            )



async def setup(bot):

    await bot.add_cog(
        Music(bot)
    )