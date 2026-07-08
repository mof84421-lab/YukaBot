import discord
from discord.ext import commands
import json
import os


FILE="data/users.json"


def load_data():

    if not os.path.exists(FILE):

        return {}

    with open(FILE,"r",encoding="utf8") as f:

        return json.load(f)



def save_data(data):

    with open(FILE,"w",encoding="utf8") as f:

        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False
        )



class Memory(commands.Cog):

    def __init__(self,bot):

        self.bot=bot



    @commands.Cog.listener()
    async def on_message(self,message):

        if message.author.bot:
            return


        data=load_data()

        uid=str(message.author.id)


        if uid not in data:

            data[uid]={
                "name":message.author.name,
                "messages":0
            }


        data[uid]["messages"]+=1


        save_data(data)



    @discord.app_commands.command(
        name="profile",
        description="ดูข้อมูลของคุณ"
    )
    async def profile(self,interaction):

        data=load_data()

        uid=str(interaction.user.id)


        msg=data.get(
            uid,
            {"messages":0}
        )


        await interaction.response.send_message(
            f"""
👤 {interaction.user.name}

💬 ข้อความ:
{msg['messages']}
"""
        )



async def setup(bot):

    await bot.add_cog(Memory(bot))