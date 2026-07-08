import discord
from discord.ext import commands
from discord import app_commands

from music.player import MusicPlayer
from music.queue import MusicQueue
from music.embeds import MusicEmbeds
from music.utils import MusicUtils


class Music(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.queue = MusicQueue()
        self.player = MusicPlayer(bot, self.queue)

    @app_commands.command(
        name="play",
        description="เล่นเพลงจาก YouTube"
    )
    async def play(
        self,
        interaction: discord.Interaction,
        query: str
    ):

        if not MusicUtils.in_voice(interaction):
            await interaction.response.send_message(
                embed=MusicEmbeds.error(
                    "กรุณาเข้าห้องเสียงก่อน"
                ),
                ephemeral=True
            )
            return

        await interaction.response.defer()

        success, result = await self.player.play(
            interaction,
            query
        )

        if not success:
            await interaction.followup.send(
                embed=MusicEmbeds.error(result)
            )
            return

        song = result["song"]

        if result["status"] == "play":

            await interaction.followup.send(
                embed=MusicEmbeds.now_playing(song)
            )

        else:

            position = self.queue.size(
                interaction.guild.id
            )

            await interaction.followup.send(
                embed=MusicEmbeds.added_queue(
                    song,
                    position
                )
            )

    @app_commands.command(
        name="pause",
        description="หยุดเพลงชั่วคราว"
    )
    async def pause(
        self,
        interaction: discord.Interaction
    ):

        if self.player.pause(interaction.guild):

            await interaction.response.send_message(
                embed=MusicEmbeds.paused()
            )

        else:

            await interaction.response.send_message(
                embed=MusicEmbeds.error(
                    "ไม่มีเพลงกำลังเล่น"
                ),
                ephemeral=True
            )

    @app_commands.command(
        name="resume",
        description="เล่นเพลงต่อ"
    )
    async def resume(
        self,
        interaction: discord.Interaction
    ):

        if self.player.resume(interaction.guild):

            await interaction.response.send_message(
                embed=MusicEmbeds.resumed()
            )

        else:

            await interaction.response.send_message(
                embed=MusicEmbeds.error(
                    "ไม่มีเพลงที่หยุดอยู่"
                ),
                ephemeral=True
            )