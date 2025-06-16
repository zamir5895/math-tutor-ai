import os
from typing import Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv


class Settings(BaseSettings):
    mongo_uri: Optional[str] = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    database_name: str = "learning_platform"
    load_dotenv()
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()