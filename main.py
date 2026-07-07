import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

@bot.event
async def on_ready():
    print(f"YukaBot Online: {bot.user}")

    await bot.change_presence(
        activity=discord.Game(
            name="ช่วยเหลือสมาชิก | !help"
        )
    )


@bot.command()
async def hello(ctx):
    await ctx.send(
        f"สวัสดี {ctx.author.mention} 💙\n"
        "ฉันคือ YukaBot"
    )


@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(
        f"🏓 Pong! {latency}ms"
    )


@bot.command()
async def server(ctx):
    guild = ctx.guild

    await ctx.send(
        f"""
📌 Server:
{guild.name}

👥 สมาชิก:
{guild.member_count}

สร้างเมื่อ:
{guild.created_at.date()}
"""
    )


@bot.event
async def on_member_join(member):
    channel = discord.utils.get(
        member.guild.text_channels,
        name="welcome"
    )

    if channel:
        await channel.send(
            f"ยินดีต้อนรับ {member.mention} 🎉"
        )


if TOKEN:
    bot.run(TOKEN)
else:
    print("ไม่พบ DISCORD_TOKEN")