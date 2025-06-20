# db/config.py
import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Extra
from dotenv import load_dotenv

# load .env before BaseSettings reads it
load_dotenv()  

class Settings(BaseSettings):
<<<<<<< HEAD
    mongo_uri: Optional[str] = os.getenv("MONGO_URI")
    youtube_api_key: Optional[str] = os.getenv("YOUTUBE_API_KEY")
    github_token: Optional[str] = os.getenv("GITHUB_TOKEN")
    database_name: str = "learning_platform"
    load_dotenv()
=======
    mongo_uri: Optional[str]      = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    youtube_api_key: Optional[str] = os.getenv("YOUTUBE_API_KEY", "YOUR_YOUTUBE_API_KEY")
    database_name: str             = "learning_platform"

>>>>>>> 2d81259d9b60f28aa685c8ea5f29805422334da7
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = Extra.ignore       # ← drop any env vars you haven’t declared

settings = Settings()
