# db/config.py
import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Extra
from dotenv import load_dotenv

# load .env before BaseSettings reads it
load_dotenv()  

class Settings(BaseSettings):
    mongo_uri: Optional[str] = os.getenv("MONGO_URI")
    youtube_api_key: Optional[str] = os.getenv("YOUTUBE_API_KEY")
    github_token: Optional[str] = os.getenv("GITHUB_TOKEN")
    database_name: str = "learning_platform"
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = Extra.ignore       # ← drop any env vars you haven’t declared

settings = Settings()
