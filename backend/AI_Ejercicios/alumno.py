from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from uuid import UUID
import uuid

class AlumnoBase(BaseModel):
    alumno_id: UUID  # Usamos UUID en lugar de ObjectId
    tema_id: UUID

class Alumno(AlumnoBase):
    id: UUID = Field(default_factory=uuid.uuid4, alias="_id")  # Usamos uuid4 para generar el UUID automáticamente

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {UUID: str}  # Aseguramos que UUID se convierta correctamente a string
