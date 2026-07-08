import discord
from discord.ext import commands
from discord import app_commands


class Ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="ticket",
        description="เปิด Ticket ติดต่อทีมงาน"
    )
    async def ticket(self, interaction: discord.Interaction):

        guild = interaction.guild

        category = discord.utils.get(
            guild.categories,
            name="TICKETS"
        )

        if category is None:
            category = await guild.create_category("TICKETS")

        channel = await guild.create_text_channel(
            f"ticket-{interaction.user.name}",
            category=category
        )

        await channel.set_permissions(
            interaction.user,
            read_messages=True,
            send_messages=True
        )

        await channel.send(
            f"🎫 {interaction.user.mention} เปิด Ticket สำเร็จ\nทีมงานจะมาตอบเร็ว ๆ นี้"
        )

        await interaction.response.send_message(
            f"✅ สร้าง Ticket แล้ว {channel.mention}",
            ephemeral=True
        )


async def setup(bot):
    await bot.add_cog(Ticket(bot))