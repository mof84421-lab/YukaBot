import discord
from discord.ext import commands
from discord import app_commands
import yt_dlp
import asyncio

YDL_OPTIONS = {
    "format": "bestaudio/best",
    "default_search": "ytsearch",
    "quiet": True,
    "noplaylist": True,
}

FFMPEG_OPTIONS = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn",
}

ytdl = yt_dlp.YoutubeDL(YDL_OPTIONS)


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = {}
        self.now_playing = {}

    async def get_source(self, query):
        loop = asyncio.get_event_loop()

        data = await loop.run_in_executor(
            None,
            lambda: ytdl.extract_info(query, download=False)
        )

        if "entries" in data:
            data = data["entries"][0]

        return {
            "title": data["title"],
            "url": data["url"],
            "webpage": data["webpage_url"],
            "thumbnail": data.get("thumbnail"),
        }

    async def play_next(self, guild):

        vc = guild.voice_client

        if guild.id not in self.queue:
            return

        if len(self.queue[guild.id]) == 0:
            self.now_playing[guild.id] = None
            return

        song = self.queue[guild.id].pop(0)

        self.now_playing[guild.id] = song

        source = discord.FFmpegPCMAudio(
            song["url"],
            **FFMPEG_OPTIONS
        )

        def after_play(error):
            asyncio.run_coroutine_threadsafe(
                self.play_next(guild),
                self.bot.loop
            )

        vc.play(source, after=after_play)