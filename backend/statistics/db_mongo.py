from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "learning_platform")

client = AsyncIOMotorClient(MONGO_URI)
db = client[MONGO_DB_NAME]

# Colecciones usadas para estadísticas
progresos_collection = db.get_collection("progresos")
reportes_collection = db.get_collection("reportes")
alumnos_collection = db.get_collection("alumnos")
temas_collection = db.get_collection("temas")
