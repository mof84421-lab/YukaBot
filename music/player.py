import discord
import asyncio

from .youtube import YouTube


FFMPEG_OPTIONS = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn",
}


class MusicPlayer:

    def __init__(self, bot, queue):
        self.bot = bot
        self.queue = queue
        self.now_playing = {}

    async def connect(self, interaction):

        if interaction.user.voice is None:
            return None

        channel = interaction.user.voice.channel

        vc = interaction.guild.voice_client

        if vc is None:
            vc = await channel.connect()

        elif vc.channel != channel:
            await vc.move_to(channel)

        return vc

    async def play(self, interaction, query):

        vc = await self.connect(interaction)

        if vc is None:
            return False, "❌ กรุณาเข้าห้องเสียงก่อน"

        song = await YouTube.search(query)

        guild_id = interaction.guild.id

        if vc.is_playing() or vc.is_paused():

            self.queue.add(guild_id, song)

            return True, {
                "status": "queue",
                "song": song
            }

        self.now_playing[guild_id] = song

        source = discord.FFmpegPCMAudio(
            song["url"],
            **FFMPEG_OPTIONS
        )

        def after(error):
            asyncio.run_coroutine_threadsafe(
                self.play_next(interaction.guild),
                self.bot.loop
            )

        vc.play(source, after=after)

        return True, {
            "status": "play",
            "song": song
        }

    async def play_next(self, guild):

        vc = guild.voice_client

        if vc is None:
            return

        song = self.queue.next(guild.id)

        if song is None:
            self.now_playing[guild.id] = None
            return

        self.now_playing[guild.id] = song

        source = discord.FFmpegPCMAudio(
            song["url"],
            **FFMPEG_OPTIONS
        )

        def after(error):
            asyncio.run_coroutine_threadsafe(
                self.play_next(guild),
                self.bot.loop
            )

        vc.play(source, after=after)

    def pause(self, guild):

        vc = guild.voice_client

        if vc and vc.is_playing():
            vc.pause()
            return True

        return False

    def resume(self, guild):

        vc = guild.voice_client

        if vc and vc.is_paused():
            vc.resume()
            return True

        return False

    def skip(self, guild):

        vc = guild.voice_client

        if vc and (vc.is_playing() or vc.is_paused()):
            vc.stop()
            return True

        return False

    async def stop(self, guild):

        vc = guild.voice_client

        if vc:

            self.queue.clear(guild.id)

            self.now_playing[guild.id] = None

            await vc.disconnect()

            return True

        return False

    def current(self, guild_id):

        return self.now_playing.get(guild_id)