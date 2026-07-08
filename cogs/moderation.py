import discord
from discord.ext import commands


LOG_CHANNEL = "bot-log"


class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    async def send_log(self, guild, message):

        channel = discord.utils.get(
            guild.text_channels,
            name=LOG_CHANNEL
        )

        if channel:
            await channel.send(message)


    @discord.app_commands.command(
        name="clear",
        description="ลบข้อความ"
    )
    @discord.app_commands.checks.has_permissions(
        manage_messages=True
    )
    async def clear(
        self,
        interaction: discord.Interaction,
        amount: int
    ):

        await interaction.channel.purge(
            limit=amount
        )

        await interaction.response.send_message(
            f"🧹 ลบ {amount} ข้อความแล้ว",
            ephemeral=True
        )


        await self.send_log(
            interaction.guild,
            f"🧹 {interaction.user} ลบ {amount} ข้อความ"
        )



    @discord.app_commands.command(
        name="kick",
        description="เตะสมาชิก"
    )
    @discord.app_commands.checks.has_permissions(
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
            f"👢 เตะ {member} แล้ว"
        )


        await self.send_log(
            interaction.guild,
            f"👢 {interaction.user} เตะ {member}\nเหตุผล: {reason}"
        )



    @discord.app_commands.command(
        name="ban",
        description="แบนสมาชิก"
    )
    @discord.app_commands.checks.has_permissions(
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
            f"🔨 แบน {member} แล้ว"
        )


        await self.send_log(
            interaction.guild,
            f"🔨 {interaction.user} แบน {member}\nเหตุผล: {reason}"
        )



    @discord.app_commands.command(
        name="warn",
        description="เตือนสมาชิก"
    )
    @discord.app_commands.checks.has_permissions(
        manage_messages=True
    )
    async def warn(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str
    ):

        await interaction.response.send_message(
            f"⚠️ เตือน {member}\nเหตุผล: {reason}"
        )


        await self.send_log(
            interaction.guild,
            f"⚠️ {interaction.user} เตือน {member}\nเหตุผล: {reason}"
        )



async def setup(bot):

    await bot.add_cog(Moderation(bot))