from typing import List, Optional
from pydantic import BaseModel, Field
from bson import ObjectId
from alumno import PyObjectId
from enum import Enum 

class PreguntaNivel(BaseModel):
    pregunta: str
    respuesta_correcta: str
    es_multiple_choice: bool = False 
    opciones: Optional[List[str]] = None
    pista: Optional[str] = None
    concepto_principal: Optional[str] = None

class NivelEnum(str, Enum):
    facil = "facil"
    medio = "medio"
    dificil = "dificil"

class NivelTema(BaseModel):
    nivel: NivelEnum
    preguntas: List[PreguntaNivel]

class TemaBase(BaseModel):
    nombre: str
    descripcion: str
    niveles: List[NivelTema]

class TemaCreate(TemaBase):
    pass

class Tema(TemaBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}