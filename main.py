import discord
from discord.ext import commands
from discord.ui import Button, View
from dotenv import load_dotenv
from openai import OpenAI
import os
import json


# =====================
# LOAD SETTINGS
# =====================

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")


client = OpenAI(
    api_key=OPENAI_KEY
)


# =====================
# DATA FILE
# =====================

DATA_FILES = {
    "memory.json": {},
    "level.json": {},
    "warnings.json": {}
}


for file, default in DATA_FILES.items():

    if not os.path.exists(file):

        with open(
            file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                default,
                f,
                indent=4,
                ensure_ascii=False
            )



# =====================
# BOT SETUP
# =====================

intents = discord.Intents.default()

intents.message_content = True
intents.members = True


bot = commands.Bot(
    command_prefix="/",
    intents=intents
)


VERIFY_ROLE = "สมาชิก"



# =====================
# READY
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
    interaction: discord.Interaction
):

    await interaction.response.send_message(
        f"สวัสดี {interaction.user.mention} 💙\n"
        "ฉันคือ Yuka AI"
    )



@bot.tree.command(
    name="ping",
    description="เช็คความเร็ว"
)
async def ping(
    interaction: discord.Interaction
):

    ms = round(
        bot.latency * 1000
    )


    await interaction.response.send_message(
        f"🏓 Pong! {ms}ms"
    )



# =====================
# AI SYSTEM
# =====================


@bot.tree.command(
    name="ask",
    description="ถาม Yuka AI"
)
async def ask(
    interaction: discord.Interaction,
    message: str
):

    await interaction.response.defer()


    try:

        response = client.chat.completions.create(

            model="gpt-4.1-mini",

            messages=[

                {
                    "role": "system",
                    "content":
                    """
                    คุณคือ Yuka AI Assistant

                    บุคลิก:
                    - เป็นมิตร
                    - ช่วยเหลือผู้ใช้
                    - พูดภาษาไทย
                    - เรียกตัวเองว่า Yuka
                    """
                },

                {
                    "role": "user",
                    "content": message
                }

            ]
        )


        answer = response.choices[0].message.content


        await interaction.followup.send(
            "💙 Yuka:\n" + answer
        )


    except Exception as e:

        await interaction.followup.send(
            "❌ AI Error\n" + str(e)
        )# =====================
# MEMORY SYSTEM
# =====================


@bot.tree.command(
    name="remember",
    description="ให้ Yuka จำข้อมูล"
)
async def remember(
    interaction: discord.Interaction,
    text: str
):

    user_id = str(
        interaction.user.id
    )


    with open(
        "memory.json",
        encoding="utf-8"
    ) as f:

        memory = json.load(f)



    if user_id not in memory:

        memory[user_id] = []



    memory[user_id].append(
        text
    )



    with open(
        "memory.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            memory,
            f,
            indent=4,
            ensure_ascii=False
        )


    await interaction.response.send_message(
        "💙 Yuka จำข้อมูลนี้แล้ว"
    )



@bot.tree.command(
    name="memory",
    description="ดูความจำของ Yuka"
)
async def memory(
    interaction: discord.Interaction
):

    user_id = str(
        interaction.user.id
    )


    with open(
        "memory.json",
        encoding="utf-8"
    ) as f:

        data = json.load(f)



    memories = data.get(
        user_id,
        []
    )


    if not memories:

        await interaction.response.send_message(
            "💙 ยังไม่มีข้อมูลที่จำไว้"
        )

        return



    await interaction.response.send_message(
        "🧠 ความจำของ Yuka:\n\n"
        + "\n".join(memories)
    )



# =====================
# LEVEL SYSTEM
# =====================


@bot.event
async def on_message(message):

    if message.author.bot:
        return


    with open(
        "level.json",
        encoding="utf-8"
    ) as f:

        levels = json.load(f)



    user_id = str(
        message.author.id
    )


    if user_id not in levels:

        levels[user_id] = {
            "xp": 0,
            "level": 1
        }



    levels[user_id]["xp"] += 5



    if levels[user_id]["xp"] >= 100:

        levels[user_id]["level"] += 1
        levels[user_id]["xp"] = 0


        await message.channel.send(
            f"🎉 {message.author.mention}\n"
            f"Level Up เป็น Level {levels[user_id]['level']}"
        )



    with open(
        "level.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            levels,
            f,
            indent=4
        )


    await bot.process_commands(message)



# =====================
# VERIFY SYSTEM
# =====================


class VerifyView(View):

    def __init__(self):

        super().__init__(
            timeout=None
        )


    @discord.ui.button(
        label="✅ ยืนยันตัวตน",
        style=discord.ButtonStyle.green,
        custom_id="verify"
    )
    async def verify(
        self,
        interaction: discord.Interaction,
        button: Button
    ):


        role = discord.utils.get(
            interaction.guild.roles,
            name=VERIFY_ROLE
        )


        if role is None:

            await interaction.response.send_message(
                "❌ ไม่พบ Role สมาชิก",
                ephemeral=True
            )

            return



        await interaction.user.add_roles(
            role
        )


        await interaction.response.send_message(
            "🎉 ยืนยันตัวตนสำเร็จ!",
            ephemeral=True
        )



@bot.tree.command(
    name="verify",
    description="สร้างปุ่มยืนยันตัวตน"
)
async def verify(
    interaction: discord.Interaction
):

    embed = discord.Embed(
        title="🔐 ระบบยืนยันตัวตน",
        description=
        "กดปุ่มเพื่อรับยศสมาชิก",
        color=0x00ff00
    )


    await interaction.response.send_message(
        embed=embed,
        view=VerifyView()
    )



# =====================
# WELCOME SYSTEM
# =====================


@bot.event
async def on_member_join(member):

    channel = discord.utils.get(
        member.guild.text_channels,
        name="welcome"
    )


    if channel:

        await channel.send(
            f"🎉 ยินดีต้อนรับ {member.mention} "
            "เข้าสู่เซิร์ฟเวอร์ 💙"
        )# =====================
# MODERATION
# =====================


@bot.tree.command(
    name="clear",
    description="ลบข้อความ"
)
async def clear(
    interaction: discord.Interaction,
    amount: int
):

    if not interaction.user.guild_permissions.manage_messages:

        await interaction.response.send_message(
            "❌ ไม่มีสิทธิ์ใช้คำสั่งนี้",
            ephemeral=True
        )

        return


    await interaction.channel.purge(
        limit=amount
    )


    await interaction.response.send_message(
        f"🧹 ลบข้อความ {amount} ข้อความแล้ว",
        ephemeral=True
    )



# =====================
# KICK
# =====================


@bot.tree.command(
    name="kick",
    description="เตะสมาชิก"
)
async def kick(
    interaction: discord.Interaction,
    member: discord.Member,
    reason: str = "ไม่มีเหตุผล"
):

    if not interaction.user.guild_permissions.kick_members:

        await interaction.response.send_message(
            "❌ ไม่มีสิทธิ์",
            ephemeral=True
        )

        return


    await member.kick(
        reason=reason
    )


    await interaction.response.send_message(
        f"👢 เตะ {member.mention} แล้ว\n"
        f"เหตุผล: {reason}"
    )



# =====================
# BAN
# =====================


@bot.tree.command(
    name="ban",
    description="แบนสมาชิก"
)
async def ban(
    interaction: discord.Interaction,
    member: discord.Member,
    reason: str = "ไม่มีเหตุผล"
):

    if not interaction.user.guild_permissions.ban_members:

        await interaction.response.send_message(
            "❌ ไม่มีสิทธิ์",
            ephemeral=True
        )

        return


    await member.ban(
        reason=reason
    )


    await interaction.response.send_message(
        f"🔨 แบน {member.mention} แล้ว"
    )



# =====================
# WARN SYSTEM
# =====================


@bot.tree.command(
    name="warn",
    description="เตือนสมาชิก"
)
async def warn(
    interaction: discord.Interaction,
    member: discord.Member,
    reason: str
):

    if not interaction.user.guild_permissions.manage_messages:

        await interaction.response.send_message(
            "❌ ไม่มีสิทธิ์",
            ephemeral=True
        )

        return



    with open(
        "warnings.json",
        encoding="utf-8"
    ) as f:

        warnings = json.load(f)



    uid = str(
        member.id
    )


    if uid not in warnings:

        warnings[uid] = []



    warnings[uid].append(
        reason
    )



    with open(
        "warnings.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            warnings,
            f,
            indent=4,
            ensure_ascii=False
        )


    await interaction.response.send_message(
        f"⚠️ เตือน {member.mention}\n"
        f"เหตุผล: {reason}"
    )



# =====================
# VIEW WARNINGS
# =====================


@bot.tree.command(
    name="warnings",
    description="ดูคำเตือนสมาชิก"
)
async def warnings(
    interaction: discord.Interaction,
    member: discord.Member
):

    with open(
        "warnings.json",
        encoding="utf-8"
    ) as f:

        data = json.load(f)



    result = data.get(
        str(member.id),
        []
    )


    if not result:

        await interaction.response.send_message(
            f"✅ {member.mention} ไม่มีคำเตือน"
        )

        return



    await interaction.response.send_message(
        "⚠️ คำเตือน:\n"
        + "\n".join(result)
    )



# =====================
# RUN BOT
# =====================


if TOKEN:

    bot.run(
        TOKEN
    )

else:

    print(
        "❌ ไม่พบ DISCORD_TOKEN"
    )