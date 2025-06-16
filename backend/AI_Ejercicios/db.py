from motor.motor_asyncio import AsyncIOMotorClient
from bson.codec_options import CodecOptions
from bson.binary import UuidRepresentation
from dotenv import load_dotenv
import os

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI") 

client = AsyncIOMotorClient(MONGO_URI)
database = client.learning_platform

uuid_codec_options = CodecOptions(uuid_representation=UuidRepresentation.STANDARD)

alumnos_collection = database.get_collection("alumnos").with_options(codec_options=uuid_codec_options)
temas_collection = database.get_collection("temas").with_options(codec_options=uuid_codec_options)
progresos_collection = database.get_collection("progresos").with_options(codec_options=uuid_codec_options)
reportes_collection = database.get_collection("reportes").with_options(codec_options=uuid_codec_options)

respuestas_collection = database.get_collection("respuestas").with_options(codec_options=uuid_codec_options)