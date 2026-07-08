import discord

from discord.ext import commands
from discord import app_commands


class Welcome(commands.Cog):

    def __init__(self, bot):

        self.bot = bot


    @commands.Cog.listener()
    async def on_member_join(self, member):

        channel = discord.utils.get(
            member.guild.text_channels,
            name="welcome"
        )

        if channel:

            embed = discord.Embed(
                title="🎉 ยินดีต้อนรับ!",
                description=
                f"สวัสดี {member.mention}\n"
                "ขอให้สนุกกับเซิร์ฟเวอร์ของเรา!",
                color=0x00ff99
            )

            embed.set_thumbnail(
                url=member.display_avatar.url
            )

            await channel.send(
                embed=embed
            )



    @app_commands.command(
        name="welcome",
        description="ทดสอบระบบต้อนรับ"
    )
    async def welcome(
        self,
        interaction: discord.Interaction
    ):

        await interaction.response.send_message(
            "✅ ระบบ Welcome พร้อมใช้งาน"
        )



async def setup(bot):

    await bot.add_cog(
        Welcome(bot)
    )