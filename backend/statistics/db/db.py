from motor.motor_asyncio import AsyncIOMotorClient
from db.config import settings


from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

client = AsyncIOMotorClient(settings.mongo_uri)
database = client[settings.database_name]
stats_ejercicio_profesor_collection = database.get_collection("stats_ejercicio_profesor")
stats_subtema_profesor_collection = database.get_collection("stats_subtema_profesor")
stats_nivel_subtema_profesor_collection = database.get_collection("stats_nivel_subtema_profesor")
stats_tema_profesor_collection = database.get_collection("stats_tema_profesor")
stats_salon_profesor_collection = database.get_collection("stats_salon_profesor")
stats_alumno_profesor_collection = database.get_collection("stats_alumno_profesor")
stats_subtema_alumno_collection = database.get_collection("stats_subtema_alumno")
stats_subtema_por_nivel_alumno_collection = database.get_collection("stats_subtema_por_nivel_alumno")
stats_tema_alumno_collection = database.get_collection("stats_tema_alumno")
stats_alumno_coleccion = database.get_collection("stats_alumno")