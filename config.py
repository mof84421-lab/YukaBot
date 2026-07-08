import os
from dotenv import load_dotenv


load_dotenv()


TOKEN = os.getenv(
    "DISCORD_TOKEN"
)


OPENAI_KEY = os.getenv(
    "OPENAI_API_KEY"
)


if TOKEN is None:

    raise Exception(
        "ไม่พบ DISCORD_TOKEN ใน .env"
    )