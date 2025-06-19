from datetime import datetime
from ..db.db import database
from ..repositorio.statsProfesorRepositorio import (
    StatsEjercicioProfesorRepository,
    StatsSubtemaProfesorRepository,
    StatsNivelSubtemaProfesorRepository,
    StatsTemaProfesorRepository,
    StatsSalonProfesorRepository,
    StatsAlumnoProfesorRepository
)
from ..schemas.schema import (
    statsPorEejercicioBaseParaProfesor,
    statsPorSubtemaBaseParaProfesor,
    StatsPorNivelSubtemaBaseParaProfesor,
    statsPorTemaBaseParaProfesor,
    statsPorSalonBaseParaProfesor,
    statsPorAlumnoBaseParaProfesor
)


class StatsProfesorService:
    def __init__(self):
        # Initialize repositories with the MongoDB database
        self.ejercicio_repo = StatsEjercicioProfesorRepository(database)
        self.subtema_repo = StatsSubtemaProfesorRepository(database)
        self.nivel_subtema_repo = StatsNivelSubtemaProfesorRepository(database)
        self.tema_repo = StatsTemaProfesorRepository(database)
        self.salon_repo = StatsSalonProfesorRepository(database)
        self.alumno_repo = StatsAlumnoProfesorRepository(database)

    # Create operations
    async def create_stats_ejercicio(self, data: statsPorEejercicioBaseParaProfesor):
        try:
            return await self.ejercicio_repo.create(data.dict())
        except Exception as e:
            print(f"Error creating stats ejercicio profesor: {e}")
            return None

    async def create_stats_subtema(self, data: statsPorSubtemaBaseParaProfesor):
        try:
            return await self.subtema_repo.create(data.dict())
        except Exception as e:
            print(f"Error creating stats subtema profesor: {e}")
            return None

    async def create_stats_nivel_subtema(self, data: StatsPorNivelSubtemaBaseParaProfesor):
        try:
            return await self.nivel_subtema_repo.create(data.dict())
        except Exception as e:
            print(f"Error creating stats nivel subtema profesor: {e}")
            return None

    async def create_stats_tema(self, data: statsPorTemaBaseParaProfesor):
        try:
            return await self.tema_repo.create(data.dict())
        except Exception as e:
            print(f"Error creating stats tema profesor: {e}")
            return None

    async def create_stats_salon(self, data: statsPorSalonBaseParaProfesor):
        try:
            return await self.salon_repo.create(data.dict())
        except Exception as e:
            print(f"Error creating stats salon profesor: {e}")
            return None

    async def create_stats_alumno(self, data: statsPorAlumnoBaseParaProfesor):
        try:
            return await self.alumno_repo.create(data.dict())
        except Exception as e:
            print(f"Error creating stats alumno profesor: {e}")
            return None

    # Read operations by _id
    async def get_stats_ejercicio_by_id(self, id: str):
        try:
            return await self.ejercicio_repo.get_by_id(id)
        except Exception as e:
            print(f"Error retrieving stats ejercicio by id: {e}")
            return None

    async def get_stats_subtema_by_id(self, id: str):
        try:
            return await self.subtema_repo.get_by_id(id)
        except Exception as e:
            print(f"Error retrieving stats subtema by id: {e}")
            return None

    async def get_stats_nivel_subtema_by_id(self, id: str):
        try:
            return await self.nivel_subtema_repo.get_by_id(id)
        except Exception as e:
            print(f"Error retrieving stats nivel subtema by id: {e}")
            return None

    async def get_stats_tema_by_id(self, id: str):
        try:
            return await self.tema_repo.get_by_id(id)
        except Exception as e:
            print(f"Error retrieving stats tema by id: {e}")
            return None

    async def get_stats_salon_by_id(self, id: str):
        try:
            return await self.salon_repo.get_by_id(id)
        except Exception as e:
            print(f"Error retrieving stats salon by id: {e}")
            return None

    async def get_stats_alumno_by_id(self, id: str):
        try:
            return await self.alumno_repo.get_by_id(id)
        except Exception as e:
            print(f"Error retrieving stats alumno by id: {e}")
            return None

    # Example of filtered query: get by subtema and tema
    async def get_stats_subtema_by_filters(self, subtema_id: str, tema_id: str):
        try:
            results = await self.subtema_repo.get_all({"subtema_id": subtema_id, "tema_id": tema_id})
            return results[0] if results else None
        except Exception as e:
            print(f"Error retrieving stats subtema by filters: {e}")
            return None

    async def get_stats_tema_by_filters(self, tema_id: str):
        try:
            results = await self.tema_repo.get_all({"tema_id": tema_id})
            return results[0] if results else None
        except Exception as e:
            print(f"Error retrieving stats tema by filters: {e}")
            return None

    async def get_stats_salon_by_filters(self, salon_id: str):
        try:
            results = await self.salon_repo.get_all({"salon_id": salon_id})
            return results[0] if results else None
        except Exception as e:
            print(f"Error retrieving stats salon by filters: {e}")
            return None
