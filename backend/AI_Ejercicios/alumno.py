from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from uuid import UUID
import uuid

class AlumnoBase(BaseModel):
    alumno_id: UUID  
    tema_id: UUID

class Alumno(AlumnoBase):
    id: UUID = Field(default_factory=uuid.uuid4, alias="_id")  
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {UUID: str} 
