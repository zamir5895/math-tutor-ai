from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv() 

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "learning_platform")

class MongoDB:
    def __init__(self, uri=MONGO_URI):
        self.client = AsyncIOMotorClient(uri)
        self.db = self.client[MONGO_DB_NAME]

mongo = MongoDB()