import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise RuntimeError("❌ ไม่พบ DISCORD_TOKEN ใน Environment Variables")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print("=" * 40)
    print(f"✅ YukaBot Online: {bot.user}")
    print("=" * 40)

    try:
        synced = await bot.tree.sync()
        print(f"✅ Sync Slash Commands: {len(synced)}")
    except Exception as e:
        print(f"❌ Sync Error: {e}")


async def load_cogs():
    if not os.path.isdir("cogs"):
        print("⚠️ ไม่พบโฟลเดอร์ cogs")
        return

    for file in os.listdir("cogs"):
        if file.endswith(".py"):
            try:
                await bot.load_extension(f"cogs.{file[:-3]}")
                print(f"✅ โหลด {file} สำเร็จ")
            except Exception as e:
                print(f"❌ โหลด {file} ไม่สำเร็จ: {e}")


async def main():
    async with bot:
        await load_cogs()

        try:
            await bot.start(TOKEN)
        except discord.LoginFailure:
            print("❌ Bot Token ไม่ถูกต้อง")
        except discord.HTTPException as e:
            print(f"❌ Discord HTTP Error: {e.status} - {e}")
        except Exception as e:
            print(f"❌ Error: {e}")


asyncio.run(main())