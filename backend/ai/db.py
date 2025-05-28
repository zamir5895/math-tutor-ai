from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

MOGO_URI = os.getenv("MONGO_URI")

client = AsyncIOMotorClient(MOGO_URI)
database = client.learning_platform

alumnos_collection = database.get_collection("alumnos")
temas_collection = database.get_collection("temas")
progresos_collection = database.get_collection("progresos")
reportes_collection = database.get_collection("reportes")