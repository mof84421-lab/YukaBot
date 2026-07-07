import discord
from discord.ext import commands
from discord.ui import Button, View
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

# ตั้งค่า Intent
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

VERIFY_ROLE_NAME = "สมาชิก"


# เมื่อบอทออนไลน์
@bot.event
async def on_ready():
    print(f"✅ YukaBot ออนไลน์แล้ว: {bot.user}")

    await bot.change_presence(
        activity=discord.Game(
            name="ช่วยเหลือสมาชิก | !help"
        )
    )


# คำสั่งทดสอบ
@bot.command()
async def hello(ctx):
    await ctx.send(
        f"สวัสดี {ctx.author.mention} 💙\n"
        "ฉันคือ YukaBot"
    )


@bot.command()
async def ping(ctx):
    ping = round(bot.latency * 1000)

    await ctx.send(
        f"🏓 Pong! {ping}ms"
    )


# ระบบ Verify
class VerifyButton(View):

    def __init__(self):
        super().__init__(timeout=None)


    @discord.ui.button(
        label="✅ ยืนยันตัวตน",
        style=discord.ButtonStyle.green,
        custom_id="verify_button"
    )
    async def verify(
        self,
        interaction: discord.Interaction,
        button: Button
    ):

        role = discord.utils.get(
            interaction.guild.roles,
            name=VERIFY_ROLE_NAME
        )

        if role is None:
            await interaction.response.send_message(
                "❌ ไม่พบยศ สมาชิก กรุณาแจ้งแอดมิน",
                ephemeral=True
            )
            return


        if role in interaction.user.roles:

            await interaction.response.send_message(
                "คุณยืนยันตัวตนแล้ว ✅",
                ephemeral=True
            )

            return


        await interaction.user.add_roles(role)


        await interaction.response.send_message(
            "🎉 ยืนยันตัวตนสำเร็จ!\n"
            "คุณได้รับยศสมาชิกแล้ว",
            ephemeral=True
        )



# สร้างข้อความ Verify
@bot.command()
@commands.has_permissions(administrator=True)
async def verify(ctx):

    embed = discord.Embed(
        title="🔐 ระบบยืนยันตัวตน",
        description=
        "ยินดีต้อนรับเข้าสู่เซิร์ฟเวอร์ 🎉\n\n"
        "กรุณากดปุ่มด้านล่างเพื่อยืนยันตัวตน\n"
        "เพื่อรับยศสมาชิกและใช้งานเซิร์ฟเวอร์",
        color=0x00ff00
    )


    await ctx.send(
        embed=embed,
        view=VerifyButton()
    )



# ต้อนรับสมาชิกใหม่
@bot.event
async def on_member_join(member):

    channel = discord.utils.get(
        member.guild.text_channels,
        name="welcome"
    )

    if channel:

        await channel.send(
            f"🎉 ยินดีต้อนรับ {member.mention} "
            "เข้าสู่เซิร์ฟเวอร์!"
        )



# เริ่มบอท
if TOKEN:
    bot.run(TOKEN)

else:
    print(
        "❌ ไม่พบ DISCORD_TOKEN"
    )