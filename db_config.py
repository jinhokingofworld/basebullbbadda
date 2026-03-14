import os

from dotenv import load_dotenv
from pymongo import MongoClient


load_dotenv()

DATABASE_NAME = "Splint2_Database"
MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise RuntimeError(
        "MONGO_URI is not set. Create a .env file from .env.example or export it in your environment."
    )

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]


def get_secret_key():
    return os.getenv("SECRET_KEY")
