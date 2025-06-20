from typing import List, Dict
from pydantic import BaseModel

class NivelStats(BaseModel):
    correctos: int
    errores: int
    total: int

class SubtemaStats(BaseModel):
    subtema_id: str
    nombre: str
    correctos: int
    errores: int
    niveles: Dict[str, NivelStats]

class TemaStats(BaseModel):
    tema_id: str
    nombre: str
    correctos: int
    errores: int
    total: int
    subtemas: List[SubtemaStats]

class ProgresoGeneral(BaseModel):
    correctos: int
    errores: int
    completados: int
    total: int
    porcentaje: float

class AlumnoStats(BaseModel):
    alumno_id: str
    progreso_general: ProgresoGeneral
    temas: List[TemaStats]
    updated_at: str

class NivelDificultad(BaseModel):
    alumno_id: str
    salon_id: str
    progreso_general: ProgresoGeneral
    margen: int
    updated_at: str


class ProgresoBase:
    pass