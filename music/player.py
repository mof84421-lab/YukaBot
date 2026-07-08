import discord



class MusicPlayer:


    def __init__(
        self,
        bot,
        queue
    ):

        self.bot = bot

        self.queue = queue



    async def play_next(
        self,
        guild
    ):

        song = self.queue.remove()


        if song:

            voice = guild.voice_client


            if voice:

                voice.play(
                    discord.FFmpegPCMAudio(
                        song
                    )
                )