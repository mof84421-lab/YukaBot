import discord
from discord.ext import commands


class Ticket(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @discord.app_commands.command(
        name="ticket",
        description="เปิด Ticket ติดต่อทีมงาน"
    )
    async def ticket(
        self,
        interaction: discord.Interaction
    ):

        guild = interaction.guild


        category = discord.utils.get(
            guild.categories,
            name="TICKETS"
        )


        if category is None:
            category = await guild.create_category(
                "TICKETS"
            )


        channel = await guild.create_text_channel(
            name=f"ticket-{interaction.user.name}",
            category=category
        )


        await channel.set_permissions(
            interaction.user,
            view_channel=True,
            send_messages=True
        )


        await channel.send(
            f"""
🎫 Ticket เปิดแล้ว

ผู้แจ้ง:
{interaction.user.mention}

ทีมงานจะมาตอบเร็ว ๆ นี้

ใช้:
/close-ticket
เพื่อปิด Ticket
"""
        )


        await interaction.response.send_message(
            f"สร้าง Ticket แล้ว: {channel.mention}",
            ephemeral=True
        )



    @discord.app_commands.command(
        name="close-ticket",
        description="ปิด Ticket"
    )
    async def close_ticket(
        self,
        interaction: discord.Interaction
    ):

        if interaction.channel.name.startswith("ticket-"):

            await interaction.response.send_message(
                "🔒 ปิด Ticket ใน 5 วินาที"
            )

            await discord.utils.sleep_until(
                discord.utils.utcnow()
            )

            await interaction.channel.delete()

        else:

            await interaction.response.send_message(
                "❌ ใช้คำสั่งนี้ใน Ticket เท่านั้น",
                ephemeral=True
            )



async def setup(bot):

    await bot.add_cog(Ticket(bot))