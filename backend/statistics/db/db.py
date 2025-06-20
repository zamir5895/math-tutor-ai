from motor.motor_asyncio import AsyncIOMotorClient

class MongoDB:
    def __init__(self, uri="mongodb://localhost:27017", db_name="learning_platform"):
        self.client = AsyncIOMotorClient(uri)
        self.db = self.client[db_name]

mongo = MongoDB()