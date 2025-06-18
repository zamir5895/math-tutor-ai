from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, Filter, FieldCondition,MatchValue
from config import settings
import numpy as np

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
        self.client.create_payload_index(
            collection_name=self.collection,
            field_name="user_id",
            field_schema="keyword"
        )

    def upsert_context(self, user_id: str, text: str, embedding: list, metadata: dict = None):
        from uuid import uuid4
        point = {
            "id": str(uuid4()),
            "vector": embedding,
            "payload": {
                "user_id": user_id,
                "text": text,
                "metadata": metadata or {}
            }
        }
        self.client.upsert(
            collection_name=self.collection,
            points=[point]
        )

    def search_context(self, user_id: str, query_embedding: list, limit: int = 3, ):
        return self.client.search(
            collection_name=self.collection,
            query_vector=query_embedding,
            query_filter=Filter(
                must=[
                    FieldCondition(
                        key="user_id",
                        match=MatchValue(value=user_id)
                    )
                ]
            ),
            limit=limit
        )
qdrant = QdrantService()