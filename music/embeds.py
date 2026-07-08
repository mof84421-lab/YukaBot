import discord

class MusicEmbeds:

    @staticmethod
    def now_playing(song):

        embed = discord.Embed(
            title="🎵 กำลังเล่น",
            description=f"**{song['title']}**",
            color=discord.Color.green()
        )

        embed.url = song["webpage"]

        if song.get("thumbnail"):
            embed.set_thumbnail(url=song["thumbnail"])

        embed.add_field(
            name="👤 ช่อง",
            value=song.get("uploader", "Unknown"),
            inline=True
        )

        embed.add_field(
            name="⏱️ ระยะเวลา",
            value=song.get("duration", "Unknown"),
            inline=True
        )

        embed.set_footer(text="Yuka Music")

        return embed


    @staticmethod
    def added_queue(song, position):

        embed = discord.Embed(
            title="📃 เพิ่มเข้าคิวแล้ว",
            description=f"**{song['title']}**",
            color=discord.Color.blurple()
        )

        embed.url = song["webpage"]

        if song.get("thumbnail"):
            embed.set_thumbnail(url=song["thumbnail"])

        embed.add_field(
            name="ลำดับในคิว",
            value=str(position),
            inline=False
        )

        return embed


    @staticmethod
    def queue(songs):

        embed = discord.Embed(
            title="🎶 คิวเพลง",
            color=discord.Color.orange()
        )

        if len(songs) == 0:
            embed.description = "ไม่มีเพลงในคิว"
            return embed

        text = ""

        for i, song in enumerate(songs, start=1):
            text += f"**{i}.** {song['title']}\n"

        embed.description = text[:4000]

        return embed


    @staticmethod
    def error(message):

        return discord.Embed(
            title="❌ Error",
            description=message,
            color=discord.Color.red()
        )


    @staticmethod
    def success(message):

        return discord.Embed(
            title="✅ สำเร็จ",
            description=message,
            color=discord.Color.green()
        )


    @staticmethod
    def paused():

        return discord.Embed(
            title="⏸️ หยุดเพลงชั่วคราว",
            color=discord.Color.gold()
        )


    @staticmethod
    def resumed():

        return discord.Embed(
            title="▶️ เล่นเพลงต่อ",
            color=discord.Color.green()
        )


    @staticmethod
    def skipped():

        return discord.Embed(
            title="⏭️ ข้ามเพลง",
            color=discord.Color.orange()
        )


    @staticmethod
    def stopped():

        return discord.Embed(
            title="⏹️ หยุดเพลง",
            description="บอทออกจากห้องเสียงแล้ว",
            color=discord.Color.red()
        )