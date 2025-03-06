import ast
import os
from dotenv import load_dotenv

class Settings():
    AUTH_FAKE_USER = os.getenv('AUTH_FAKE_USER')
    AUTH_FAKE_PASSWORD = os.getenv('AUTH_FAKE_PASSWORD')
    AUTH_HASHED_PASSWORD = os.getenv('AUTH_HASHED_PASSWORD')
    SECRET_KEY = os.getenv('AUTH_SECRET_KEY')
    ALGORITHM = os.getenv('AUTH_JWT_ALGORITHM')
    ACCESS_TOKEN_EXPIRE_MIN = os.getenv('AUTH_ACCESS_TOKEN_EXPIRE_MIN')

load_dotenv()
settings = Settings()