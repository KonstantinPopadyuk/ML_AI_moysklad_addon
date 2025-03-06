import ast
import os
from dotenv import load_dotenv

class Settings():
    MOYSKALD_LOGIN = os.getenv('MOYSKALD_LOGIN')
    MOYSKLAD_PASSWORD = os.getenv('MOYSKLAD_PASSWORD')
    MOYSKLAD_TOKEN = os.getenv('MOYSKLAD_TOKEN')

    POSTGRES_SERVER = os.getenv('POSTGRES_SERVER')
    POSTGRES_USER = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_DB = os.getenv('POSTGRES_DB')
    SQLALCHEMY_DATABASE_URL = os.getenv('SQLALCHEMY_DATABASE_URL', 
        f"postgresql+asyncpg://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}")
    SQLALCHEMY_SYNC_DB_URL = os.getenv('SQLALCHEMY_SYNC_DB_URL')

    DB_USER = os.getenv('DB_USER')
    DB_PASS = os.getenv('DB_PASS')

load_dotenv()
settings = Settings()