import discord
from discord.ext import commands
from discord import app_commands


BAD_WORDS = [
    "คำหยาบ1",
    "คำหยาบ2"
]


class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot



    # กันคำหยาบ
    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return


        content = message.content.lower()


        for word in BAD_WORDS:

            if word in content:

                await message.delete()


                await message.channel.send(
                    f"⚠️ {message.author.mention} กรุณาใช้คำสุภาพ"
                )


                return



    # ลบข้อความ
    @app_commands.command(
        name="clear",
        description="ลบข้อความ"
    )
    @app_commands.default_permissions(
        manage_messages=True
    )
    async def clear(
        self,
        interaction: discord.Interaction,
        amount:int
    ):


        await interaction.response.defer(
            ephemeral=True
        )


        await interaction.channel.purge(
            limit=amount
        )


        await interaction.followup.send(
            f"🧹 ลบแล้ว {amount} ข้อความ"
        )



    # Warn
    @app_commands.command(
        name="warn",
        description="เตือนสมาชิก"
    )
    @app_commands.default_permissions(
        manage_messages=True
    )
    async def warn(
        self,
        interaction:discord.Interaction,
        member:discord.Member,
        reason:str
    ):


        await interaction.response.send_message(
            f"⚠️ {member.mention} ถูกเตือน\nเหตุผล: {reason}"
        )



    # Kick
    @app_commands.command(
        name="kick",
        description="เตะสมาชิก"
    )
    @app_commands.default_permissions(
        kick_members=True
    )
    async def kick(
        self,
        interaction:discord.Interaction,
        member:discord.Member,
        reason:str="ไม่มีเหตุผล"
    ):


        await member.kick(
            reason=reason
        )


        await interaction.response.send_message(
            f"👢 เตะ {member.name} แล้ว"
        )



    # Ban
    @app_commands.command(
        name="ban",
        description="แบนสมาชิก"
    )
    @app_commands.default_permissions(
        ban_members=True
    )
    async def ban(
        self,
        interaction:discord.Interaction,
        member:discord.Member,
        reason:str="ไม่มีเหตุผล"
    ):


        await member.ban(
            reason=reason
        )


        await interaction.response.send_message(
            f"🔨 แบน {member.name} แล้ว"
        )



async def setup(bot):

    await bot.add_cog(
        Moderation(bot)
    )