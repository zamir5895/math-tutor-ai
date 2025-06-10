from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional

class RespuestaAlumnoBase(BaseModel):
    alumno_id: UUID
    tema_id: UUID
    pregunta_id: UUID
    respuesta: str
    respuesta_correcta: bool
    fecha_respuesta: datetime = Field(default_factory=datetime.utcnow)


class RespuestaAlumnoCreate(BaseModel):
    alumno_id: UUID 
    tema_id: UUID    
    pregunta_id: UUID  
    respuesta: str
    fecha_respuesta: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {
            UUID: str,
            datetime: lambda v: v.isoformat()
        }


class RespuestaAlumnoResponse(RespuestaAlumnoBase):
    id: UUID

    class Config:
        json_encoders = {
            UUID: str,
            datetime: lambda v: v.isoformat()
        }
