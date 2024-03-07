from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY")


class TestConfig(Config):
    TESTING = True
