import discord


class MusicUtils:

    @staticmethod
    def in_voice(interaction: discord.Interaction):

        return interaction.user.voice is not None


    @staticmethod
    def same_voice(interaction: discord.Interaction):

        vc = interaction.guild.voice_client

        if vc is None:
            return True

        if interaction.user.voice is None:
            return False

        return vc.channel == interaction.user.voice.channel


    @staticmethod
    def voice_client(guild):

        return guild.voice_client


    @staticmethod
    def is_playing(guild):

        vc = guild.voice_client

        return vc is not None and vc.is_playing()


    @staticmethod
    def is_paused(guild):

        vc = guild.voice_client

        return vc is not None and vc.is_paused()


    @staticmethod
    def can_control(interaction):

        if interaction.user.voice is None:
            return False

        vc = interaction.guild.voice_client

        if vc is None:
            return False

        return vc.channel == interaction.user.voice.channel


    @staticmethod
    def format_duration(seconds):

        if seconds is None:
            return "00:00"

        seconds = int(seconds)

        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60

        if hours > 0:
            return f"{hours:02}:{minutes:02}:{secs:02}"

        return f"{minutes:02}:{secs:02}"


    @staticmethod
    def volume_check(volume):

        if volume < 0:
            volume = 0

        if volume > 100:
            volume = 100

        return volume


    @staticmethod
    def queue_position(queue):

        return len(queue) + 1