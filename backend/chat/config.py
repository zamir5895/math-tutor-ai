from pydantic import Field
from pydantic_settings import BaseSettings
from functools import lru_cache
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    qdrant_url: str = os.getenv("QDRANT_URL", "http://localhost:6333")
    qdrant_collection: str = os.getenv("QDRANT_COLLECTION", "default_collection")
    qdrant_api_key: str = os.getenv("QDRANT_API_KEY", "")
    
    mongo_uri: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    mongo_db: str = os.getenv("MONGO_DB", "default_db")

    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")

@lru_cache()
def get_settings() -> Settings:
    return Settings()
settings = get_settings()