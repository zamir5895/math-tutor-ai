from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from typing import Any, Dict, List, Optional
from ..db.db import (
    stats_alumno_coleccion,
    stats_tema_alumno_collection,
    stats_subtema_por_nivel_alumno_collection,
    stats_subtema_alumno_collection
)

from ..schemas.schema import (
    statsPorNivelSubtemaBaseParaAlumno,
    statsSubtemaBaseParaAlumno,
    statsTemaBaseParaAlumno,
    statsAlumnoBase,
)

def fix_objectid(doc):
        if not doc:
            return doc
        doc = dict(doc)
        if "_id" in doc:
            doc["_id"] = str(doc["_id"])
        return doc


class StatsNivelSubtemaAlumnoRepository:
    def __init__(self):
        pass

    async def create(self, data: statsPorNivelSubtemaBaseParaAlumno):
        try:
            data = data.dict()
            result = await stats_subtema_por_nivel_alumno_collection.insert_one(data)
            r = fix_objectid(result)
            return
        except Exception as e:
            print(f"Error creating stats_nivel_subtema_alumno: {e}")
            return None

    async def get_by_alumno_subtema_nivel(self, alumno_id: str, subtema_id: str):
        try:
            doc = await stats_subtema_por_nivel_alumno_collection.find_one({"alumno_id": alumno_id, "subtema_id": subtema_id})
            if doc:
                return doc
            return None
        except Exception as e:
            print(f"Error getting stats_nivel_subtema_alumno: {e}")
            return None

    async def get_all(self, filter: Dict[str, Any] = {}) :
        try:
            docs = stats_subtema_por_nivel_alumno_collection.find(filter)
            return docs
        except Exception as e:
            print(f"Error getting all stats_nivel_subtema_alumno: {e}")
            return []

    async def update_by_alumno_subtema_nivel(self, alumno_id: str, subtema_id: str, nivel: str, data: Dict[str, Any]):
        try:
            await stats_subtema_por_nivel_alumno_collection.update_one(
                {"alumno_id": alumno_id, "subtema_id": subtema_id, "nivel": nivel},
                {"$set": data}
            )
            return await self.get_by_alumno_subtema_nivel(alumno_id, subtema_id, nivel)
        except Exception as e:
            print(f"Error updating stats_nivel_subtema_alumno: {e}")
            return None

    async def delete_by_alumno_subtema_nivel(self, alumno_id: str, subtema_id: str, nivel: str) -> bool:
        try:
            result = await self.collection.delete_one({"alumno_id": alumno_id, "subtema_id": subtema_id, "nivel": nivel})
            return result.deleted_count == 1
        except Exception as e:
            print(f"Error deleting stats_nivel_subtema_alumno: {e}")
            return False

class StatsSubtemaAlumnoRepository:
    def __init__(self):
        pass

    async def create(self, data: statsSubtemaBaseParaAlumno):
        try:
            data = data.dict()
            result = await stats_subtema_alumno_collection.insert_one(data)
            res = fix_objectid(result)
            return res
        except Exception as e:
            print(f"Error creating stats_subtema_alumno: {e}")
            return None

    async def get_by_alumno_subtema(self, alumno_id: str, subtema_id: str) :
        try:
            doc = await stats_subtema_alumno_collection.find_one({"alumno_id": alumno_id, "subtema_id": subtema_id})
            if doc:
                return doc
            return None
        except Exception as e:
            print(f"Error getting stats_subtema_alumno: {e}")
            return None

    async def get_all(self, filter: Dict[str, Any] = {}):
        try:
            docs = stats_subtema_alumno_collection.find(filter)
            if docs:
                return docs
            return []
        except Exception as e:
            print(f"Error getting all stats_subtema_alumno: {e}")
            return []

    async def update_by_alumno_subtema(self, alumno_id: str, subtema_id: str, data: Dict[str, Any]) :
        try:
            await stats_subtema_alumno_collection.update_one(
                {"alumno_id": alumno_id, "subtema_id": subtema_id},
                {"$set": data}
            )
            return await self.get_by_alumno_subtema(alumno_id, subtema_id)
        except Exception as e:
            print(f"Error updating stats_subtema_alumno: {e}")
            return None

    async def delete_by_alumno_subtema(self, alumno_id: str, subtema_id: str) -> bool:
        try:
            result = await stats_subtema_alumno_collection.delete_one({"alumno_id": alumno_id, "subtema_id": subtema_id})
            return result.deleted_count == 1
        except Exception as e:
            print(f"Error deleting stats_subtema_alumno: {e}")
            return False

# stats_tema_alumno
class StatsTemaAlumnoRepository:
    def __init__(self):
        pass

    async def create(self, data: statsTemaBaseParaAlumno) :
        try:
            data=data.dict()
            result = await stats_tema_alumno_collection.insert_one(data)
            res = fix_objectid(result)
            return res
        except Exception as e:
            print(f"Error creating stats_tema_alumno: {e}")
            return None

    async def get_by_alumno_tema(self, alumno_id: str, tema_id: str) :
        try:
            doc = await stats_tema_alumno_collection.find_one({"alumno_id": alumno_id, "tema_id": tema_id}) 
            if doc:
                return fix_objectid(doc)
            return None
        except Exception as e:
            print(f"Error getting stats_tema_alumno: {e}")
            return None

    async def get_all(self, filter: Dict[str, Any] = {}) :
        try:
            docs = stats_tema_alumno_collection.find(filter)
            if docs:
                return docs
            return []
        except Exception as e:
            print(f"Error getting all stats_tema_alumno: {e}")
            return []

    async def update_by_alumno_tema(self, alumno_id: str, tema_id: str, data: Dict[str, Any]) :
        try:
            await stats_tema_alumno_collection.update_one(
                {"alumno_id": alumno_id, "tema_id": tema_id},
                {"$set": data}
            )
            return await self.get_by_alumno_tema(alumno_id, tema_id)
        except Exception as e:
            print(f"Error updating stats_tema_alumno: {e}")
            return None

    async def delete_by_alumno_tema(self, alumno_id: str, tema_id: str) -> bool:
        try:
            result = await stats_tema_alumno_collection.delete_one({"alumno_id": alumno_id, "tema_id": tema_id})
            return result.deleted_count == 1
        except Exception as e:
            print(f"Error deleting stats_tema_alumno: {e}")
            return False

# stats_alumno
class StatsAlumnoRepository:
    def __init__(self):
        pass

    async def create(self, data: statsAlumnoBase):
        try:
            data = data.dict()
            result = await stats_alumno_coleccion.insert_one(data)
            res = fix_objectid(result)
            return res
        except Exception as e:
            print(f"Error creating stats_alumno: {e}")
            return None

    async def get_by_alumno_id(self, alumno_id: str) :
        try:
            doc = await stats_alumno_coleccion.find_one({"alumno_id": alumno_id})
            if doc:
                return doc
            return None
        except Exception as e:
            print(f"Error getting stats_alumno: {e}")
            return None

    async def get_all(self, filter: Dict[str, Any] = {}) :
        try:
            docs = stats_alumno_coleccion.find(filter)
            if docs:
                return docs
            return []
        except Exception as e:
            print(f"Error getting all stats_alumno: {e}")
            return []

    async def update_by_alumno_id(self, alumno_id: str, data: Dict[str, Any]) :
        try:
            await stats_alumno_coleccion.update_one(
                {"alumno_id": alumno_id},
                {"$set": data}
            )
            return await self.get_by_alumno_id(alumno_id)
        except Exception as e:
            print(f"Error updating stats_alumno: {e}")
            return None

    async def delete_by_alumno_id(self, alumno_id: str) -> bool:
        try:
            result = await stats_alumno_coleccion.delete_one({"alumno_id": alumno_id})
            return result.deleted_count == 1
        except Exception as e:
            print(f"Error deleting stats_alumno: {e}")
            return False