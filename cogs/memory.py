from discord.ext import commands
from discord import app_commands
import json
import os


FILE="data/memory.json"


if not os.path.exists("data"):
    os.makedirs("data")


if not os.path.exists(FILE):
    with open(FILE,"w") as f:
        json.dump({},f)



class Memory(commands.Cog):

    def __init__(self,bot):
        self.bot=bot



    @app_commands.command(
        name="remember",
        description="ให้ Yuka จำ"
    )
    async def remember(
        self,
        interaction,
        text:str
    ):

        with open(FILE,"r") as f:
            data=json.load(f)


        uid=str(interaction.user.id)

        data.setdefault(uid,[])

        data[uid].append(text)


        with open(FILE,"w") as f:
            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False
            )


        await interaction.response.send_message(
            "🧠 จำแล้ว"
        )



async def setup(bot):

    await bot.add_cog(Memory(bot))