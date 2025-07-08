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

    def get_conversation_context(self, user_id: str, conversation_id: str, last_n_messages: int = 10):
        """Obtiene el contexto reciente de una conversación específica"""
        conversation = self.conversations.find_one(
            {"user_id": user_id, "conversation_id": conversation_id},
            {"messages": {"$slice": -last_n_messages}, "title": 1, "created_at": 1}
        )
        return conversation
    
    def get_user_conversation_summary(self, user_id: str, limit: int = 20):
        """Obtiene un resumen de las conversaciones del usuario"""
        conversations = self.conversations.find(
            {"user_id": user_id},
            {"conversation_id": 1, "title": 1, "updated_at": 1, "messages": {"$slice": -1}}
        ).sort("updated_at", -1).limit(limit)
        
        summary = []
        for conv in conversations:
            last_message = conv.get("messages", [{}])[-1] if conv.get("messages") else {}
            summary.append({
                "conversation_id": conv.get("conversation_id"),
                "title": conv.get("title", "Sin título"),
                "last_message": last_message.get("content", "")[:100] + "..." if len(last_message.get("content", "")) > 100 else last_message.get("content", ""),
                "last_updated": conv.get("updated_at"),
                "message_count": len(conv.get("messages", []))
            })
        return summary
    
    def update_conversation_metadata(self, user_id: str, conversation_id: str, metadata: dict):
        """Actualiza metadatos de una conversación"""
        self.conversations.update_one(
            {"user_id": user_id, "conversation_id": conversation_id},
            {"$set": {"metadata": metadata, "updated_at": datetime.utcnow()}}
        )
    
    def search_user_messages(self, user_id: str, query: str, limit: int = 10):
        """Busca mensajes del usuario por contenido"""
        pipeline = [
            {"$match": {"user_id": user_id}},
            {"$unwind": "$messages"},
            {"$match": {"messages.content": {"$regex": query, "$options": "i"}}},
            {"$sort": {"messages.timestamp": -1}},
            {"$limit": limit},
            {"$project": {
                "conversation_id": 1,
                "title": 1,
                "message": "$messages",
                "relevance_score": {"$meta": "textScore"}
            }}
        ]
        return list(self.conversations.aggregate(pipeline))
    
    def get_user_chat_statistics(self, user_id: str):
        """Obtiene estadísticas de chat del usuario"""
        pipeline = [
            {"$match": {"user_id": user_id}},
            {"$group": {
                "_id": "$user_id",
                "total_conversations": {"$sum": 1},
                "total_messages": {"$sum": {"$size": "$messages"}},
                "first_conversation": {"$min": "$created_at"},
                "last_activity": {"$max": "$updated_at"},
                "avg_messages_per_conversation": {"$avg": {"$size": "$messages"}}
            }}
        ]
        result = list(self.conversations.aggregate(pipeline))
        return result[0] if result else {
            "total_conversations": 0,
            "total_messages": 0,
            "avg_messages_per_conversation": 0
        }

mongo = MongoService()