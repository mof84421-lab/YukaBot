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

            view_channel=True,

            send_messages=True

        )


        embed = discord.Embed(

            title="🎫 Ticket เปิดแล้ว",

            description=
            f"""
ผู้สร้าง:
{interaction.user.mention}

ทีมงานจะมาตอบกลับเร็ว ๆ นี้
""",

            color=0x00ffff

        )


        await channel.send(

            embed=embed

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

        interaction: discord.Interaction

    ):


        if interaction.channel.name.startswith(
            "ticket-"
        ):


            await interaction.response.send_message(

                "🔒 ปิด Ticket แล้ว"

            )


            await interaction.channel.delete()


        else:


            await interaction.response.send_message(

                "❌ ใช้คำสั่งนี้ในห้อง Ticket เท่านั้น",

                ephemeral=True

            )



async def setup(bot):

    await bot.add_cog(
        Ticket(bot)
    )