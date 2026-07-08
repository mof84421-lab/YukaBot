from discord.ext import commands
from discord import app_commands


class Verify(commands.Cog):

    def __init__(self,bot):
        self.bot=bot


    @app_commands.command(
        name="verify",
        description="ยืนยันตัวตน"
    )
    async def verify(self,interaction):

        role = discord.utils.get(
            interaction.guild.roles,
            name="สมาชิก"
        )

        if role:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(
                "✅ ยืนยันแล้ว"
            )


async def setup(bot):
    await bot.add_cog(Verify(bot))