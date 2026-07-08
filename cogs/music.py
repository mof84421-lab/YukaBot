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
        self.player = MusicPlayer(
            bot,
            self.queue
        )


    async def safe_send_error(self, interaction, text):

        embed = MusicEmbeds.error(text)

        if interaction.response.is_done():

            await interaction.followup.send(
                embed=embed,
                ephemeral=True
            )

        else:

            await interaction.response.send_message(
                embed=embed,
                ephemeral=True
            )


    @app_commands.command(
        name="play",
        description="เล่นเพลงจาก YouTube"
    )
    async def play(
        self,
        interaction: discord.Interaction,
        query: str
    ):

        if interaction.guild is None:
            return

        if not MusicUtils.in_voice(interaction):

            await self.safe_send_error(
                interaction,
                "กรุณาเข้าห้องเสียงก่อน"
            )
            return


        await interaction.response.defer()


        try:

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


        except Exception as e:

            print(
                f"[PLAY ERROR] {e}"
            )

            await interaction.followup.send(
                embed=MusicEmbeds.error(
                    "เกิดข้อผิดพลาดในการเล่นเพลง"
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

            await self.safe_send_error(
                interaction,
                "ไม่มีเพลงกำลังเล่น"
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

            await self.safe_send_error(
                interaction,
                "ไม่มีเพลงที่หยุดอยู่"
            )



    @app_commands.command(
        name="skip",
        description="ข้ามเพลง"
    )
    async def skip(
        self,
        interaction: discord.Interaction
    ):

        if self.player.skip(interaction.guild):

            await interaction.response.send_message(
                embed=MusicEmbeds.skipped()
            )

        else:

            await self.safe_send_error(
                interaction,
                "ไม่มีเพลงให้ข้าม"
            )



    @app_commands.command(
        name="stop",
        description="หยุดเพลง"
    )
    async def stop(
        self,
        interaction: discord.Interaction
    ):


        if await self.player.stop(
            interaction.guild
        ):

            await interaction.response.send_message(
                embed=MusicEmbeds.stopped()
            )

        else:

            await self.safe_send_error(
                interaction,
                "บอทยังไม่ได้อยู่ในห้องเสียง"
            )



    @app_commands.command(
        name="queue",
        description="ดูคิวเพลง"
    )
    async def queue_cmd(
        self,
        interaction: discord.Interaction
    ):

        songs = self.queue.get_queue(
            interaction.guild.id
        )

        await interaction.response.send_message(
            embed=MusicEmbeds.queue(songs)
        )



    @app_commands.command(
        name="nowplaying",
        description="เพลงที่กำลังเล่น"
    )
    async def nowplaying(
        self,
        interaction: discord.Interaction
    ):


        song = self.player.current(
            interaction.guild.id
        )


        if song is None:

            await self.safe_send_error(
                interaction,
                "ไม่มีเพลงกำลังเล่น"
            )
            return


        await interaction.response.send_message(
            embed=MusicEmbeds.now_playing(song)
        )



async def setup(bot):

    await bot.add_cog(
        Music(bot)
    )