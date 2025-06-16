from typing import Optional
from pydantic import BaseModel, Field
from bson import ObjectId
from schemas.Util import PyObjectId

class EjercicioResueltoBase(BaseModel):
    """
    Base model for resolved exercises.
    """
    ejercicio_id: str
    respuesta_usuario: str
    es_correcta: bool
    fecha_resolucion: Optional[str] = None
    tema_id: str
    subtema_id: str
    nivel: str

class EjerciciosResueltoByAlumno(BaseModel):

    alumno_id: str
    salon_id: str
    ejercicios_resueltos: list[EjercicioResueltoBase] = Field(default_factory=list)

class CreateEjercicioResuelto(EjercicioResueltoBase):
    """
    Model for creating a resolved exercise.
    """
    pass
class EjercicioResuelto(EjerciciosResueltoByAlumno):
    id: str = Field(alias="_id")

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}