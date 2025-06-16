from db.db import subtemas_collection
from bson import ObjectId
from pymongo.errors import PyMongoError
from models.Subtema import CreateSubtema, YoutubeTemasCreation

class SubTemaRepository:
    def __init__(self):
        pass    
    async def exists(self, titulo: str, tema_id: str) -> bool:
        try:
            existing_subtema = await subtemas_collection.find_one({"titulo": titulo, "tema_id": ObjectId(tema_id)})
            print("Para el tema_id:", tema_id, "y el titulo:", titulo, "existe subtema:", existing_subtema)
            return existing_subtema is not None
        except PyMongoError as e:
            return False

    async def existSubtema(self, titulo:str, subtema_id:str) -> bool:
        try:
            existing_subtema = await subtemas_collection.find_one({"titulo": titulo, "_id": ObjectId(subtema_id)})
            print("Para el subtema_id:", subtema_id, "y el titulo:", titulo, "existe subtema:", existing_subtema)
            return existing_subtema is not None
        except PyMongoError as e:
            return False

    async def createSubTema(self, subtema: CreateSubtema):
        try:
            subtema_dict = subtema.dict()
            subtema_dict["tema_id"] = ObjectId(subtema.tema_id)  
            result = await subtemas_collection.insert_one(subtema_dict)
            return str(result.inserted_id)
        except PyMongoError as e:
            return None

    async def getSubTemaById(self, id: str):
        try:
            print("Buscando subtema con ID:", id)
            subtema = await subtemas_collection.find_one({"_id": ObjectId(id)})
            print("Subtema encontrado:", subtema)
            return subtema
        except PyMongoError as e:
            return None
    
    async def getSubTemasByTemaId(self, tema_id: str):
        try:
            subtemas = await subtemas_collection.find({"tema_id": ObjectId(tema_id)}).to_list(length=None)
            return subtemas
        except PyMongoError as e:
            return []
        
    async def addVideoToSubTema(self, subtema_id: str, video: YoutubeTemasCreation):
        try:
            result = await subtemas_collection.update_one(
                {"_id": ObjectId(subtema_id)},
                {"$addToSet": {"video_urls": video.dict()}}
            )
            return result.modified_count > 0
        except PyMongoError as e:
            return False
        
    async def addEjercicioToSubTema(self, subtema_id: str, ejercicio_id: str, nivel: str):
        """
        Agrega el ejercicio_id al nivel correspondiente en el campo preguntas del subtema.
        """
        try:
            result = await subtemas_collection.update_one(
                {"_id": ObjectId(subtema_id)},
                {"$addToSet": {f"preguntas.{nivel}": ejercicio_id}}
            )
            return result.modified_count > 0
        except PyMongoError as e:
            return False
    async def searchSubtemas(self, query: str):
        try:
            subtemas = await subtemas_collection.find({
                "$or": [
                    {"titulo": {"$regex": query, "$options": "i"}},
                    {"descripcion": {"$regex": query, "$options": "i"}}
                ]
            }).to_list(length=None)
            return subtemas
        except PyMongoError:
            return []
    async def getEjerciciosByNivel(self, subtema_id: str, nivel: str):
        try:
            subtema = await subtemas_collection.find_one({"_id": ObjectId(subtema_id)})
            return subtema.get("preguntas", {}).get(nivel, []) if subtema else []
        except PyMongoError:
            return []
    async def getEjerciciosBySubtemaId(self, subtema_id: str):
        try:
            subtema = await subtemas_collection.find_one({"_id": ObjectId(subtema_id)})
            if not subtema:
                return []
            ejercicios = []
            for nivel, ids in subtema.get("preguntas", {}).items():
                for ejercicio_id in ids:
                    ejercicios.append({
                        "nivel": nivel,
                        "ejercicio_id": ejercicio_id
                    })
            return ejercicios
        except PyMongoError:
            return []

    async def deleteVideoFromSubTema(self, subtema_id:str, video_id: str):
        try:
            result = await subtemas_collection.update_one(
                {"_id": ObjectId(subtema_id)},
                {"$pull": {"video_urls": {"id": video_id}}}
            )
            return result.modified_count > 0
        except PyMongoError as e:
            return False
        
    async def deleteSubTema(self, subtema_id: str):
        try:
            result = await subtemas_collection.delete_one({"_id": ObjectId(subtema_id)})
            return result.deleted_count > 0
        except PyMongoError as e:
            return False
    
    async def removeEjercicioFromSubTema(self, subtema_id: str, ejercicio_id: str, nivel: str):
        """
        Elimina el ejercicio_id del nivel correspondiente en el campo preguntas del subtema.
        """
        try:
            result = await subtemas_collection.update_one(
                {"_id": ObjectId(subtema_id)},
                {"$pull": {f"preguntas.{nivel}": ejercicio_id}}
            )
            return result.modified_count > 0
        except PyMongoError as e:
            return False
    
    async def updateSubtemaOrden(self, subtema_id: str, orden: int):
        """
        Actualiza el orden de un subtema.
        """
        try:
            result = await subtemas_collection.update_one(
                {"_id": ObjectId(subtema_id)},
                {"$set": {"orden": orden}}
            )
            return result.modified_count > 0
        except PyMongoError as e:
            return False