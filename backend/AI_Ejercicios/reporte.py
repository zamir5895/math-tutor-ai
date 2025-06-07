from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID, uuid4
from datetime import datetime

class ReporteBase(BaseModel):
    alumno_id: UUID
    tema_id: UUID
    tema_nombre: str
    nivel_maximo: int
    respuestas_totales: int
    correctas: int
    porcentaje: float
    observaciones: str
    fecha: datetime = Field(default_factory=datetime.utcnow)

class Reporte(ReporteBase):
    id: UUID = Field(default_factory=uuid4, alias="_id")
    
    class Config:
        allow_population_by_field_name = True
        json_encoders = {
            UUID: str,
            datetime: lambda v: v.isoformat()
        }

class ReporteCreate(ReporteBase):
    pass

class ReporteUpdate(BaseModel):
    observaciones: Optional[str] = None
    fecha: datetime = Field(default_factory=datetime.utcnow)

class ReporteResponse(ReporteBase):
    id: str
    alumno_id: str
    tema_id: str
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }