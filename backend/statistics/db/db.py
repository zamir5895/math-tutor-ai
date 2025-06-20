from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv() 

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/learning_platform")

class MongoDB:
    def __init__(self, uri=MONGO_URI):
        self.client = AsyncIOMotorClient(uri)
        # Extrae el nombre de la base de datos del URI si está presente
        db_name = uri.rsplit('/', 1)[-1] if '/' in uri else "learning_platform"
        self.db = self.client[db_name]

mongo = MongoDB()