# En tema.py
from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID, uuid4
from datetime import datetime
from enum import Enum

class NivelEnum(str, Enum):
    facil = "facil"
    medio = "medio"
    dificil = "dificil"

class Pregunta(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    pregunta: str
    respuesta_correcta: str
    es_multiple_choice: bool = False
    opciones: Optional[List[str]] = None
    explicacion: Optional[str] = None

class Nivel(BaseModel):
    nivel: NivelEnum
    preguntas: List[Pregunta]

class TemaBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    niveles: List[Nivel] = []
    fecha_creacion: datetime = Field(default_factory=datetime.utcnow)
    puntos: Optional[int] = 0 
    cantidad_problemas: Optional[int] = 0 

class Tema(TemaBase):
    id: UUID = Field(default_factory=uuid4, alias="_id")
    
    class Config:
        allow_population_by_field_name = True
        json_encoders = {
            UUID: str,
            datetime: lambda v: v.isoformat()
        }

class TemaCreate(TemaBase):
    pass

class TemaUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    niveles: Optional[List[Nivel]] = None
    puntos: Optional[int] = None  
    cantidad_problemas: Optional[int] = None 

class TemaResponse(TemaBase):
    id: str
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class PreguntaCreate(BaseModel):
    pregunta: str
    respuesta_correcta: str
    es_multiple_choice: bool = False
    opciones: Optional[List[str]] = None
    explicacion: Optional[str] = None

class PreguntaUpdate(BaseModel):
    pregunta: Optional[str] = None
    respuesta_correcta: Optional[str] = None
    es_multiple_choice: Optional[bool] = None
    opciones: Optional[List[str]] = None
    explicacion: Optional[str] = None
