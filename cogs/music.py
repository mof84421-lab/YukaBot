import discord
from discord.ext import commands
from discord import app_commands

import wavelink


class Music(commands.Cog):

    def __init__(self, bot):

        self.bot = bot



    @commands.Cog.listener()
    async def on_ready(self):

        print("🎵 Music System Ready")



    @app_commands.command(
        name="play",
        description="เปิดเพลง"
    )
    async def play(
        self,
        interaction: discord.Interaction,
        search:str
    ):


        await interaction.response.defer()


        if not interaction.user.voice:

            return await interaction.followup.send(
                "❌ กรุณาเข้าห้องเสียงก่อน"
            )



        vc = interaction.guild.voice_client



        if not vc:

            vc = await interaction.user.voice.channel.connect(
                cls=wavelink.Player
            )



        tracks = await wavelink.Playable.search(
            search
        )



        if not tracks:

            return await interaction.followup.send(
                "❌ ไม่พบเพลง"
            )



        track = tracks[0]



        await vc.play(track)



        await interaction.followup.send(
            f"🎵 เล่นเพลง: **{track.title}**"
        )



    @app_commands.command(
        name="pause",
        description="หยุดเพลงชั่วคราว"
    )
    async def pause(
        self,
        interaction: discord.Interaction
    ):


        vc = interaction.guild.voice_client


        if vc:

            await vc.pause(True)


            await interaction.response.send_message(
                "⏸️ หยุดเพลงแล้ว"
            )



    @app_commands.command(
        name="resume",
        description="เล่นเพลงต่อ"
    )
    async def resume(
        self,
        interaction: discord.Interaction
    ):


        vc = interaction.guild.voice_client


        if vc:

            await vc.pause(False)


            await interaction.response.send_message(
                "▶️ เล่นต่อแล้ว"
            )



    @app_commands.command(
        name="stop",
        description="ออกจากห้องเพลง"
    )
    async def stop(
        self,
        interaction: discord.Interaction
    ):


        vc = interaction.guild.voice_client


        if vc:

            await vc.disconnect()


            await interaction.response.send_message(
                "⏹️ หยุดเพลงแล้ว"
            )



async def setup(bot):

    await bot.add_cog(
        Music(bot)
    )