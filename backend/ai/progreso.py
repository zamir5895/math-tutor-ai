from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from bson import ObjectId
from alumno import PyObjectId

class RespuestaAlumno(BaseModel):
    nivel: int
    pregunta: str
    respuesta_alumno: str
    respuesta_correcta: str
    explicacion_gpt: str
    correcto: bool
    tiempo_respuesta: Optional[int] = None  # en segundos
    intentos: int = 1
    fecha_respuesta: datetime = Field(default_factory=datetime.utcnow)

class ProgresoBase(BaseModel):
    alumno_id: PyObjectId
    tema_id: PyObjectId
    tema_nombre: str = ""
    nivel_actual: int = 1
    estado: str = "en_progreso"  # en_progreso, completado, pausado
    respuestas: List[RespuestaAlumno] = []
    fecha_inicio: datetime = Field(default_factory=datetime.utcnow)
    fecha_fin: Optional[datetime] = None
    tiempo_total: Optional[int] = None  # en minutos

class ProgresoCreate(ProgresoBase):
    pass

class Progreso(ProgresoBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}