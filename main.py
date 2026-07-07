import discord
from discord.ext import commands
from discord.ui import Button, View
from dotenv import load_dotenv
import os
import json


load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")


# สร้างไฟล์ข้อมูลอัตโนมัติ
if not os.path.exists("memory.json"):
    with open("memory.json","w",encoding="utf-8") as f:
        json.dump({},f,ensure_ascii=False)


if not os.path.exists("level.json"):
    with open("level.json","w",encoding="utf-8") as f:
        json.dump({},f)



intents = discord.Intents.default()

intents.message_content = True
intents.members = True


bot = commands.Bot(
    command_prefix="/",
    intents=intents
)



VERIFY_ROLE = "สมาชิก"



# =====================
# ONLINE
# =====================

@bot.event
async def on_ready():

    print(
        f"✅ YukaBot Online : {bot.user}"
    )


    await bot.tree.sync()


    await bot.change_presence(
        activity=discord.Game(
            "Yuka AI Assistant 💙"
        )
    )



# =====================
# BASIC COMMAND
# =====================


@bot.tree.command(
    name="hello",
    description="ทักทาย Yuka"
)
async def hello(
    interaction:discord.Interaction
):

    await interaction.response.send_message(
        f"สวัสดี {interaction.user.mention} 💙\nฉันคือ Yuka"
    )



@bot.tree.command(
    name="ping",
    description="เช็คความเร็วบอท"
)
async def ping(
    interaction:discord.Interaction
):

    ms = round(
        bot.latency*1000
    )

    await interaction.response.send_message(
        f"🏓 Pong {ms}ms"
    )



# =====================
# AI + MEMORY
# =====================


@bot.tree.command(
    name="ask",
    description="ถาม Yuka AI"
)
async def ask(
    interaction:discord.Interaction,
    message:str
):

    user=str(
        interaction.user.id
    )


    with open(
        "memory.json",
        encoding="utf-8"
    ) as f:

        data=json.load(f)


    data[user]=message


    with open(
        "memory.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False
        )


    await interaction.response.send_message(
        f"💙 Yuka จำข้อความนี้แล้ว:\n{message}"
    )



# =====================
# LEVEL SYSTEM
# =====================


@bot.event
async def on_message(message):

    if message.author.bot:
        return


    with open(
        "level.json"
    ) as f:

        data=json.load(f)


    uid=str(
        message.author.id
    )


    if uid not in data:

        data[uid]={
            "xp":0,
            "level":1
        }


    data[uid]["xp"]+=5


    if data[uid]["xp"]>=100:

        data[uid]["level"]+=1
        data[uid]["xp"]=0


        await message.channel.send(
            f"🎉 {message.author.mention} Level Up เป็น {data[uid]['level']}"
        )


    with open(
        "level.json",
        "w"
    ) as f:

        json.dump(
            data,
            f,
            indent=4
        )


    await bot.process_commands(message)



# =====================
# VERIFY BUTTON
# =====================


class VerifyView(View):

    def __init__(self):

        super().__init__(
            timeout=None
        )


    @discord.ui.button(
        label="✅ ยืนยันตัวตน",
        style=discord.ButtonStyle.green
    )
    async def verify(
        self,
        interaction,
        button
    ):


        role = discord.utils.get(
            interaction.guild.roles,
            name=VERIFY_ROLE
        )


        if role:

            await interaction.user.add_roles(role)


            await interaction.response.send_message(
                "✅ ได้รับยศสมาชิกแล้ว",
                ephemeral=True
            )

        else:

            await interaction.response.send_message(
                "❌ ไม่พบยศ สมาชิก",
                ephemeral=True
            )



@bot.tree.command(
    name="verify",
    description="สร้างระบบยืนยันตัวตน"
)
async def verify(
    interaction:discord.Interaction
):

    embed=discord.Embed(
        title="🔐 Verify",
        description="กดปุ่มเพื่อยืนยันตัวตน"
    )


    await interaction.response.send_message(
        embed=embed,
        view=VerifyView()
    )



# =====================
# MODERATION
# =====================


@bot.tree.command(
    name="clear",
    description="ลบข้อความ"
)
async def clear(
    interaction:discord.Interaction,
    amount:int
):

    if not interaction.user.guild_permissions.manage_messages:

        await interaction.response.send_message(
            "❌ ไม่มีสิทธิ์"
        )

        return


    await interaction.channel.purge(
        limit=amount
    )


    await interaction.response.send_message(
        "✅ ลบแล้ว",
        ephemeral=True
    )



# =====================
# START
# =====================

if TOKEN:

    bot.run(TOKEN)

else:

    print(
        "❌ ไม่พบ DISCORD_TOKEN"
    )