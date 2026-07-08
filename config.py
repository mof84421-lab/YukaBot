import os
from dotenv import load_dotenv

load_dotenv()


class Config:

    TOKEN = os.getenv("DISCORD_TOKEN")

    OPENAI_KEY = os.getenv(
        "OPENAI_API_KEY"
    )


config = Config()