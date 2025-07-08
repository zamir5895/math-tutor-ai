from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, Filter, FieldCondition, MatchValue
from config import settings

class QdrantService:
    def __init__(self):
        self.client = QdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key
        )
        self.collection = settings.qdrant_collection
        self._setup_collection()

    def _setup_collection(self):
        try:
            self.client.get_collection(self.collection)
        except Exception:
            self.client.create_collection(
                collection_name=self.collection,
                vectors_config=VectorParams(size=768, distance=Distance.COSINE)
            )
        
        # Crear índices para filtrado eficiente
        try:
            self.client.create_payload_index(
                collection_name=self.collection,
                field_name="user_id",
                field_schema="keyword"
            )
        except Exception:
            pass  # Índice ya existe
        
        try:
            self.client.create_payload_index(
                collection_name=self.collection,
                field_name="conversation_id",
                field_schema="keyword"
            )
        except Exception:
            pass  # Índice ya existe
            
        try:
            self.client.create_payload_index(
                collection_name=self.collection,
                field_name="context_type",
                field_schema="keyword"
            )
        except Exception:
            pass  # Índice ya existe

    def upsert_context(self, user_id: str, text: str, embedding: list, 
                      conversation_id: str = None, context_type: str = "general", 
                      metadata: dict = None):
        from uuid import uuid4
        point = {
            "id": str(uuid4()),
            "vector": embedding,
            "payload": {
                "user_id": user_id,
                "conversation_id": conversation_id,
                "context_type": context_type,  # "general" o "conversation"
                "text": text,
                "metadata": metadata or {}
            }
        }
        self.client.upsert(
            collection_name=self.collection,
            points=[point]
        )

    def search_context(self, user_id: str, query_embedding: list, 
                      conversation_id: str = None, limit: int = 5):
        # Filtros base
        filters = [
            FieldCondition(
                key="user_id",
                match=MatchValue(value=user_id)
            )
        ]
        
        # Si hay conversation_id, buscar contexto específico de la conversación
        if conversation_id:
            filters.append(
                FieldCondition(
                    key="conversation_id",
                    match=MatchValue(value=conversation_id)
                )
            )
        
        return self.client.search(
            collection_name=self.collection,
            query_vector=query_embedding,
            query_filter=Filter(must=filters),
            limit=limit
        )

    def search_general_context(self, user_id: str, query_embedding: list, limit: int = 3):
        """Busca contexto general del usuario (no específico de conversación)"""
        return self.client.search(
            collection_name=self.collection,
            query_vector=query_embedding,
            query_filter=Filter(
                must=[
                    FieldCondition(
                        key="user_id",
                        match=MatchValue(value=user_id)
                    ),
                    FieldCondition(
                        key="context_type",
                        match=MatchValue(value="general")
                    )
                ]
            ),
            limit=limit
        )

    def delete_conversation_context(self, user_id: str, conversation_id: str):
        """Elimina todo el contexto de una conversación específica"""
        self.client.delete(
            collection_name=self.collection,
            points_selector=Filter(
                must=[
                    FieldCondition(
                        key="user_id",
                        match=MatchValue(value=user_id)
                    ),
                    FieldCondition(
                        key="conversation_id",
                        match=MatchValue(value=conversation_id)
                    )
                ]
            )
        )

    def delete_context(self, user_id: str):
        """Elimina todo el contexto de un usuario"""
        self.client.delete(
            collection_name=self.collection,
            points_selector=Filter(
                must=[
                    FieldCondition(
                        key="user_id",
                        match=MatchValue(value=user_id)
                    )
                ]
            )
        )

qdrant = QdrantService()
