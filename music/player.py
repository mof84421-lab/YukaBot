import discord


class MusicPlayer:


    def __init__(self, bot):

        self.bot = bot



    async def stop(self, guild):

        voice = guild.voice_client


        if voice:

            await voice.disconnect()