from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from typing import Any, Dict, List, Optional, Type, TypeVar
from pydantic import BaseModel

from schemas.schema import (
    statsPorEejercicioBaseParaProfesor,
    statsPorSubtemaBaseParaProfesor,
    StatsPorNivelSubtemaBaseParaProfesor,
    statsPorTemaBaseParaProfesor,
    statsPorSalonBaseParaProfesor,
    statsPorAlumnoBaseParaProfesor,
)

T = TypeVar("T", bound=BaseModel)

class BaseRepository:
    def __init__(self, db: AsyncIOMotorDatabase, collection_name: str, model: Type[T]):
        self.collection = db[collection_name]
        self.model = model

    async def create(self, data: Dict[str, Any]) -> Optional[T]:
        try:
            result = await self.collection.insert_one(data)
            data["_id"] = result.inserted_id
            return self.model(**data)
        except Exception as e:
            print(f"Error creating document: {e}")
            return None

    async def get_by_id(self, id: str) -> Optional[T]:
        try:
            doc = await self.collection.find_one({"_id": ObjectId(id)})
            return self.model(**doc) if doc else None
        except Exception as e:
            print(f"Error getting document by id: {e}")
            return None

    async def get_all(self, filter: Dict[str, Any] = {}) -> List[T]:
        try:
            docs = self.collection.find(filter)
            return [self.model(**doc) async for doc in docs]
        except Exception as e:
            print(f"Error getting all documents: {e}")
            return []

    async def update(self, id: str, data: Dict[str, Any]) -> Optional[T]:
        try:
            await self.collection.update_one({"_id": ObjectId(id)}, {"$set": data})
            return await self.get_by_id(id)
        except Exception as e:
            print(f"Error updating document: {e}")
            return None

    async def delete(self, id: str) -> bool:
        try:
            result = await self.collection.delete_one({"_id": ObjectId(id)})
            return result.deleted_count == 1
        except Exception as e:
            print(f"Error deleting document: {e}")
            return False

# Repositorios para las colecciones de profesor

class StatsEjercicioProfesorRepository(BaseRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        super().__init__(db, "stats_ejercicio_profesor", statsPorEejercicioBaseParaProfesor)

class StatsSubtemaProfesorRepository(BaseRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        super().__init__(db, "stats_subtema_profesor", statsPorSubtemaBaseParaProfesor)

class StatsNivelSubtemaProfesorRepository(BaseRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        super().__init__(db, "stats_nivel_subtema_profesor", StatsPorNivelSubtemaBaseParaProfesor)

class StatsTemaProfesorRepository(BaseRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        super().__init__(db, "stats_tema_profesor", statsPorTemaBaseParaProfesor)

class StatsSalonProfesorRepository(BaseRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        super().__init__(db, "stats_salon_profesor", statsPorSalonBaseParaProfesor)

class StatsAlumnoProfesorRepository(BaseRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        super().__init__(db, "stats_alumno_profesor", statsPorAlumnoBaseParaProfesor)