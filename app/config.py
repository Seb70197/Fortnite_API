import os
from dotenv import load_dotenv

load_dotenv()

# Configuration class to hold database settings
class settings:
    DB_SERVER = os.getenv("DB_SERVER")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    API_KEY = os.getenv("API_KEY")

# Create an instance of the settings class
settings = settings()
