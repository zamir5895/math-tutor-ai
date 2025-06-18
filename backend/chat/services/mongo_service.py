from pymongo import MongoClient
from config import settings
from datetime import datetime

class MongoService:
    def __init__(self):
        self.client = MongoClient(settings.mongo_uri)
        self.db = self.client[settings.mongo_db]
        self.conversations = self.db.conversations
        self._setup_indexes()

    def _setup_indexes(self):
        self.conversations.create_index([("user_id", 1)])
        self.conversations.create_index([("conversation_id", 1)])

    def save_message(self, user_id: str, conversation_id: str, role: str, content: str):
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow()
        }
        self.conversations.update_one(
            {"user_id": user_id, "conversation_id": conversation_id},
            {"$push": {"messages": message}},
            upsert=True
        )

    def get_conversation(self, user_id: str, conversation_id: str):
        return self.conversations.find_one({
            "user_id": user_id,
            "conversation_id": conversation_id
        })

mongo = MongoService()