# import ast
import os
from dotenv import load_dotenv

class Settings():
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    KAFKA_BROKER = os.getenv('KAFKA_BROKER')

load_dotenv()
settings = Settings()