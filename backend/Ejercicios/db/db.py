from motor.motor_asyncio import AsyncIOMotorClient
from db.config import settings


from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os




client = AsyncIOMotorClient(settings.mongo_uri)
database = client[settings.database_name]
temas_collection = database.get_collection("temas")
ejercicios_collection = database.get_collection("ejercicios")
examenes_subtopicos = database.get_collection("examenes_subtopicos")
examenes_topicos = database.get_collection("examenes_topicos")
exam = database.get_collection("exam")
pdf_resource = database.get_collection("pdf_resource")
ejercicios_resueltos = database.get_collection("ejercicios_resueltos")
subtemas_collection = database.get_collection("subtemas")