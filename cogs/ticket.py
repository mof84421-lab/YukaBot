import discord

from discord.ext import commands
from discord import app_commands



class Ticket(commands.Cog):

    def __init__(self, bot):

        self.bot = bot



    @app_commands.command(
        name="ticket",
        description="สร้าง Ticket"
    )
    async def ticket(
        self,
        interaction: discord.Interaction
    ):

        guild = interaction.guild


        category = discord.utils.get(
            guild.categories,
            name="Tickets"
        )


        if category is None:

            category = await guild.create_category(
                "Tickets"
            )



        channel = await guild.create_text_channel(

            name=f"ticket-{interaction.user.name}",

            category=category

        )


        await channel.set_permissions(
            interaction.user,
            read_messages=True,
            send_messages=True
        )


        await channel.send(

            f"""
🎫 Ticket เปิดแล้ว

ผู้สร้าง:
{interaction.user.mention}

ใช้ช่องนี้ติดต่อทีมงาน
"""
        )


        await interaction.response.send_message(

            f"✅ สร้าง Ticket แล้ว {channel.mention}",

            ephemeral=True
        )



    @app_commands.command(
        name="close",
        description="ปิด Ticket"
    )
    async def close(

        self,
        interaction:discord.Interaction

    ):


        if "ticket-" in interaction.channel.name:

            await interaction.response.send_message(
                "🔒 ปิด Ticket"
            )

            await interaction.channel.delete()


        else:

            await interaction.response.send_message(
                "❌ ใช้คำสั่งนี้ใน Ticket เท่านั้น",
                ephemeral=True
            )



async def setup(bot):

    await bot.add_cog(
        Ticket(bot)
    )