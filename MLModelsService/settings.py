import ast
import os
from dotenv import load_dotenv

class Settings():
    LOGIN = os.getenv('LOGIN')
    PASSWORD = os.getenv('PASSWORD')
    TOKEN = os.getenv('TOKEN')

    POSTGRES_SERVER = os.getenv('POSTGRES_SERVER')
    POSTGRES_USER = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_DB = os.getenv('POSTGRES_DB')
    SQLALCHEMY_DATABASE_URL = os.getenv('SQLALCHEMY_DATABASE_URL', 
        f"postgresql+asyncpg://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}")
    SQLALCHEMY_SYNC_DB_URL = os.getenv('SQLALCHEMY_SYNC_DB_URL', 
        f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}")


    DB_USER = os.getenv('DB_USER')
    DB_PASS = os.getenv('DB_PASS')

    # FAKE_USERS_DB = ast.literal_eval(os.getenv('AUTH_FAKE_USERS_DB'))
    SECRET_KEY = os.getenv('AUTH_SECRET_KEY')
    ALGORITHM = os.getenv('AUTH_JWT_ALGORITHM')
    ACCESS_TOKEN_EXPIRE_MIN = os.getenv('AUTH_ACCESS_TOKEN_EXPIRE_MIN')

    DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
    DEEPSEEK_API_URL = os.getenv('DEEPSEEK_API_URL')
    DEEPSEEK_API_VERSION = os.getenv('DEEPSEEK_API_VERSION')
    DEEPSEEK_API_CHAT_MODEL = os.getenv('DEEPSEEK_API_CHAT_MODEL')
    DEEPSEEK_API_REASONER_MODEL = os.getenv('DEEPSEEK_API_REASONER_MODEL')

    LOGFIRE_API_KEY=os.getenv('LOGFIRE_API_KEY')
    LOGFIRE_PROJECT_ID=os.getenv('LOGFIRE_API_KEY')

load_dotenv()
settings = Settings()