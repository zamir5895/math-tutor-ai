from repositorio.statsAlumnoRepositorio import StatsAlumnoRepository, StatsTemaAlumnoRepository, StatsSubtemaAlumnoRepository, StatsNivelSubtemaAlumnoRepository
from datetime import datetime

class StatsAlumnoService:
    def __init__(self):
        self.stats_alumno_repository = StatsAlumnoRepository()
        self.stats_tema_alumno_repository = StatsTemaAlumnoRepository()
        self.stats_subtema_alumno_repository = StatsSubtemaAlumnoRepository()
        self.stats_nivel_subtema_alumno_repository = StatsNivelSubtemaAlumnoRepository()
    
    async def create_stats_subtema_alumno(self, data):
        try:
            return await self.stats_subtema_alumno_repository.create(data)
        except Exception as e:
            print(f"Error creating stats subtema alumno: {e}")
            return None
    async def create_stats_nivel_subtema_alumno(self, data):
        try:
            return await self.stats_nivel_subtema_alumno_repository.create(data)
        except Exception as e:
            print(f"Error creating stats nivel subtema alumno: {e}")
            return None
    async def create_stats_tema_alumno(self, data):
        try:
            return await self.stats_tema_alumno_repository.create(data)
        except Exception as e:
            print(f"Error creating stats tema alumno: {e}")
            return None
    async def create_stats_alumno(self, data):
        try:
            return await self.stats_alumno_repository.create(data)
        except Exception as e:
            print(f"Error creating stats alumno: {e}")
            return None
    async def get_stats_alumno_by_id(self, alumno_id: str, salon_id: str):
        try:
            r = await self.stats_alumno_repository.get_by_id(alumno_id)
            if not r:
                return self.create_stats_alumno({
                    "alumno_id": alumno_id,
                    "salon_id":salon_id,
                    "fecha_ultima_actividad": datetime.now().isoformat(),
                })
            return r
        except Exception as e:
            print(f"Error getting stats alumno by id: {e}")
            return None
        
    async def get_stats_tema_alumno_by_id(self, alumno_id: str, tema_id: str):
        try:
            r = await self.stats_tema_alumno_repository.get_by_alumno_tema(alumno_id, tema_id)
            if not r:
                return self.create_stats_tema_alumno({
                    "alumno_id": alumno_id,
                    "tema_id": tema_id,
                })
            return r
        except Exception as e:
            print(f"Error getting stats tema alumno by id: {e}")
            return None