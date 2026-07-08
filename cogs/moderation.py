import discord

from discord.ext import commands
from discord import app_commands



class Moderation(commands.Cog):

    def __init__(self, bot):

        self.bot = bot



    @app_commands.command(
        name="kick",
        description="เตะสมาชิก"
    )
    @app_commands.checks.has_permissions(
        kick_members=True
    )
    async def kick(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str = "ไม่มีเหตุผล"
    ):

        await member.kick(
            reason=reason
        )

        await interaction.response.send_message(
            f"✅ เตะ {member.mention} แล้ว"
        )



    @app_commands.command(
        name="ban",
        description="แบนสมาชิก"
    )
    @app_commands.checks.has_permissions(
        ban_members=True
    )
    async def ban(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str = "ไม่มีเหตุผล"
    ):

        await member.ban(
            reason=reason
        )

        await interaction.response.send_message(
            f"🔨 แบน {member.mention} แล้ว"
        )



    @app_commands.command(
        name="clear",
        description="ลบข้อความ"
    )
    @app_commands.checks.has_permissions(
        manage_messages=True
    )
    async def clear(
        self,
        interaction: discord.Interaction,
        amount:int
    ):

        await interaction.channel.purge(
            limit=amount
        )


        await interaction.response.send_message(
            f"🧹 ลบ {amount} ข้อความแล้ว",
            ephemeral=True
        )



    @app_commands.command(
        name="timeout",
        description="Timeout สมาชิก"
    )
    @app_commands.checks.has_permissions(
        moderate_members=True
    )
    async def timeout(
        self,
        interaction: discord.Interaction,
        member:discord.Member,
        minutes:int
    ):


        duration = discord.utils.utcnow()

        await member.timeout(
            discord.utils.utcnow()
            - duration
        )

        await interaction.response.send_message(
            f"⏳ Timeout {member.mention}"
        )



async def setup(bot):

    await bot.add_cog(
        Moderation(bot)
    )