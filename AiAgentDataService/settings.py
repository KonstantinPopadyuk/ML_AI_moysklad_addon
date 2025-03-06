import ast
import os
from dotenv import load_dotenv

class Settings():
    DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
    DEEPSEEK_API_URL = os.getenv('DEEPSEEK_API_URL')
    DEEPSEEK_API_VERSION = os.getenv('DEEPSEEK_API_VERSION')
    DEEPSEEK_API_CHAT_MODEL = os.getenv('DEEPSEEK_API_CHAT_MODEL')
    DEEPSEEK_API_REASONER_MODEL = os.getenv('DEEPSEEK_API_REASONER_MODEL')

    LOGFIRE_API_KEY=os.getenv('LOGFIRE_API_KEY')
    LOGFIRE_PROJECT_ID=os.getenv('LOGFIRE_API_KEY')
    KAFKA_BROKER=os.getenv('KAFKA_BROKER')

load_dotenv()
settings = Settings()