from discord.ext import commands
from discord import app_commands

import database



class Memory(commands.Cog):

    def __init__(self,bot):

        self.bot = bot

        database.setup()



    @app_commands.command(
        name="remember",
        description="ให้ Yuka จำข้อมูล"
    )
    async def remember(
        self,
        interaction,
        text:str
    ):


        database.add_memory(
            str(interaction.user.id),
            text
        )


        await interaction.response.send_message(
            "🧠 Yuka จำข้อมูลนี้แล้ว"
        )



    @app_commands.command(
        name="memory",
        description="ดูความจำของ Yuka"
    )
    async def memory(
        self,
        interaction
    ):


        data = database.get_memory(
            str(interaction.user.id)
        )


        if data:

            await interaction.response.send_message(
                "🧠 สิ่งที่ Yuka จำได้:\n"
                +
                "\n".join(data)
            )

        else:

            await interaction.response.send_message(
                "ยังไม่มีข้อมูลที่จำ"
            )



async def setup(bot):

    await bot.add_cog(
        Memory(bot)
    )