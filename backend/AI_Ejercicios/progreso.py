from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID, uuid4
from datetime import datetime

class RespuestaAlumno(BaseModel):
    nivel: int
    pregunta: str
    respuesta_alumno: str
    explicacion_gpt: str
    correcto: bool
    fecha_respuesta: datetime = Field(default_factory=datetime.utcnow)

class ProgresoBase(BaseModel):
    alumno_id: UUID
    tema_id: UUID
    nivel_actual: int = 1
    respuestas: List[RespuestaAlumno] = []
    estado: str = "en_progreso"  # en_progreso, completado, pausado
    fecha_inicio: datetime = Field(default_factory=datetime.utcnow)
    fecha_actualizacion: datetime = Field(default_factory=datetime.utcnow)

class Progreso(ProgresoBase):
    id: UUID = Field(default_factory=uuid4, alias="_id")
    
    class Config:
        allow_population_by_field_name = True
        json_encoders = {
            UUID: str,
            datetime: lambda v: v.isoformat()
        }

class ProgresoCreate(ProgresoBase):
    pass

class ProgresoUpdate(BaseModel):
    nivel_actual: Optional[int] = None
    estado: Optional[str] = None
    fecha_actualizacion: datetime = Field(default_factory=datetime.utcnow)

class ProgresoResponse(ProgresoBase):
    id: str
    alumno_id: str
    tema_id: str
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }