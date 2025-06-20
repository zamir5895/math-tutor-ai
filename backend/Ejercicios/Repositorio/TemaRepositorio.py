from db.db import temas_collection
from bson import ObjectId
from pymongo.errors import PyMongoError
from models.Temas import CreateTema
class TemaRepository:
    def __init__(self):
        pass
    async def exists(self, nombre: str, curso_id: str):
        try:
            existing_tema = await temas_collection.find_one({"nombre": nombre, "classroom_id": curso_id})
            return existing_tema is not None
        except PyMongoError as e:
            return False

    async def _verificar_tema_existe(self, tema: str) -> bool:
        try:
            tema_existente = await temas_collection.find_one(
                {"nombre": {"$regex": f"^{tema}$", "$options": "i"}}
            )
            return tema_existente is not None
        except PyMongoError as e:
            return False

    async def getTemasBySalonId(self, classroom_id: str):
        try:
            temas = await temas_collection.find({"classroom_id": classroom_id}).to_list(length=None)
            return temas
        except PyMongoError as e:
            return []

    async def getTemaById(self, id: str):
        try:
            tema = await temas_collection.find_one({"_id": ObjectId(id)})
            return tema
        except PyMongoError as e:
            return None

    async def addSubTemaToTema(self, tema_id: str, subtema_id: str):
        try:
            result = await temas_collection.update_one(
                {"_id": ObjectId(tema_id)},
                {"$addToSet": {"subtema_id": (subtema_id)}}
            )
            return result.modified_count > 0
        except PyMongoError as e:
            return False
    
    async def createTema(self,tema:CreateTema):
        try:
            tema_dict = tema.dict(by_alias=True)
            result = await temas_collection.insert_one(tema_dict)
            return str(result.inserted_id) 

        except PyMongoError as e:
            return None

    async def deleteTema(self, tema_id: str):
        try:
            result = await temas_collection.delete_one({"_id": ObjectId(tema_id)})
            return result.deleted_count > 0
        except PyMongoError as e:
            return False
        
    async def getTemaByNombre(self, nombre: str):
        try:
            tema = await temas_collection.find_one({"nombre": {"$regex": f"^{nombre}$", "$options": "i"}})
            return tema
        except PyMongoError as e:
            return None
    
    async def removeSubTemaFromTema(self, tema_id:str, subtema_id: str):
        try:
            result = await temas_collection.update_one(
                {"_id": ObjectId(tema_id)},
                {"$pull": {"subtema_id": subtema_id}}
            )
            return result.modified_count > 0
        except PyMongoError as e:
            return False
    
    async def updateTemaOrder(self, tema_id: str, new_order: int):
        try:
            result = await temas_collection.update_one(
                {"_id": ObjectId(tema_id)},
                {"$set": {"orden": new_order}}
            )
            return result.modified_count > 0
        except PyMongoError as e:
            return False

    async def getTemaBySubtemaId(self, subtema_id: str):
        try:
            tema = await temas_collection.find_one({"subtema_id": subtema_id})
            return tema
        except PyMongoError as e:
            return None