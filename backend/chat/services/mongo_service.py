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
        self.conversations.create_index([("user_id", 1), ("updated_at", -1)])

    def save_message(self, user_id: str, conversation_id: str, role: str, content: str):
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow()
        }
        
        # Actualizar conversación con el nuevo mensaje
        self.conversations.update_one(
            {"user_id": user_id, "conversation_id": conversation_id},
            {
                "$push": {"messages": message},
                "$set": {"updated_at": datetime.utcnow()},
                "$setOnInsert": {"created_at": datetime.utcnow()}
            },
            upsert=True
        )

    def set_conversation_title(self, user_id: str, conversation_id: str, title: str):
        """Establece el título de una conversación"""
        self.conversations.update_one(
            {"user_id": user_id, "conversation_id": conversation_id},
            {"$set": {"title": title}}
        )

    def get_conversation(self, user_id: str, conversation_id: str):
        return self.conversations.find_one({
            "user_id": user_id,
            "conversation_id": conversation_id
        })

    def delete_conversation(self, user_id: str, conversation_id: str):
        """Elimina una conversación"""
        result = self.conversations.delete_one({
            "user_id": user_id,
            "conversation_id": conversation_id
        })
        return result.deleted_count > 0

    def get_conversations_list(self, user_id: str):
        """Obtiene lista de conversaciones con información resumida"""
        return self.conversations.find(
            {"user_id": user_id},
            {"_id": 0, "conversation_id": 1, "title": 1, "messages": {"$slice": -1}, "updated_at": 1}
        ).sort("updated_at", -1)

mongo = MongoService()