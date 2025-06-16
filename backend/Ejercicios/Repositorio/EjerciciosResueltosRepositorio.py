from db.db import ejercicios_resueltos
from bson import ObjectId

class EjercicioResueltosRepository:
    def __init__(self):
        pass

    def fix_objectid(self, doc):
        if not doc:
            return doc
        doc = dict(doc)
        if "_id" in doc:
            doc["_id"] = str(doc["_id"])
            if "alumno_id" in doc:
                doc["alumno_id"] = str(doc["alumno_id"])
                if "ejercicios_resueltos" in doc:
                    for ejercicio in doc["ejercicios_resueltos"]:
                        if isinstance(ejercicio, dict) and "ejercicio_id" in ejercicio:
                            ejercicio["ejercicio_id"] = str(ejercicio["ejercicio_id"])
        return doc

    async def add_ejercicio_resuelto(self, alumno_id: str,salon_id:str, ejercicio_resuelto: dict):
        try:
            result = await ejercicios_resueltos.update_one(
                {"alumno_id": alumno_id, "salon_id": salon_id},

                {"$push": {"ejercicios_resueltos": ejercicio_resuelto}},
                upsert=True
            )
            return result.modified_count > 0 or result.upserted_id is not None
        except Exception as e:
            print(f"Error al agregar el ejercicio resuelto: {e}")
            return False
    
    async def get_ejercicios_resueltos_by_alumno_id(self, alumno_id: str):
        try:
            ejercicio_resuelto = await ejercicios_resueltos.find_one({"alumno_id": alumno_id})
            if ejercicio_resuelto:
                return self.fix_objectid(ejercicio_resuelto)
            return None
        except Exception as e:
            print(f"Error al obtener los ejercicios resueltos: {e}")
            return None
    
    async def get_cantidad_de_ejercicios_resueltos_by_salon_id(self, salon_id: str):
        try:
            count = await ejercicios_resueltos.count_documents({"salon_id": salon_id})
            return count
        except Exception as e:
            print(f"Error al contar los ejercicios resueltos: {e}")
            return 0
    async def get_ejercicios_resueltos_by_salon_id(self, salon_id: str):
        try:
            docs = await ejercicios_resueltos.find({"salon_id": salon_id}).to_list(length=None)
            return [self.fix_objectid(doc) for doc in docs]
        except Exception as e:
            print(f"Error al obtener los ejercicios resueltos por salón: {e}")
            return []
    
    async def remove_ejercicio_resuelto(self, alumno_id: str, ejercicio_id: str):
        try:
            result = await ejercicios_resueltos.update_one(
                {"alumno_id": alumno_id},
                {"$pull": {"ejercicios_resueltos": {"ejercicio_id": ejercicio_id}}}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Error al eliminar el ejercicio resuelto: {e}")
            return False
    async def update_ejercicio_resuelto(self, alumno_id: str, ejercicio_id: str, update_data: dict):
        try:
            result = await ejercicios_resueltos.update_one(
                {"alumno_id": alumno_id, "ejercicios_resueltos.ejercicio_id": ejercicio_id},
                {"$set": {f"ejercicios_resueltos.$.{k}": v for k, v in update_data.items()}}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Error al actualizar el ejercicio resuelto: {e}")
            return False
    async def get_ejercicios_resueltos_by_alumno_and_subtema(self, alumno_id: str, subtema_id: str):
        try:
            doc = await ejercicios_resueltos.find_one({"alumno_id": alumno_id})
            if doc and "ejercicios_resueltos" in doc:
                ejercicios = [
                    ej for ej in doc["ejercicios_resueltos"] if ej.get("subtema_id") == subtema_id
                ]
                return ejercicios
            return []
        except Exception as e:
            print(f"Error al filtrar ejercicios resueltos: {e}")
            return []