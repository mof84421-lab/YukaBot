import os
from dotenv import load_dotenv

# โหลดค่า .env หรือ Render Environment
load_dotenv()


class Config:

    def __init__(self):

        # Discord Token
        self.TOKEN = os.getenv(
            "DISCORD_TOKEN"
        )

        # OpenAI API Key
        self.OPENAI_KEY = os.getenv(
            "OPENAI_API_KEY"
        )


        # ตรวจสอบ Discord Token

        if not self.TOKEN:
            raise ValueError(
                "❌ ไม่พบ DISCORD_TOKEN\n"
                "กรุณาเพิ่ม DISCORD_TOKEN ใน Render Environment หรือไฟล์ .env"
            )


# เรียกใช้งาน Config
config = Config()