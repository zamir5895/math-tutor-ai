from typing import List, Optional, Dict
from pydantic import BaseModel, Field
from bson import ObjectId
from enum import Enum 
from schemas.Util import PyObjectId

class NivelEnum(str, Enum):
    facil = "facil"
    medio = "medio"
    dificil = "dificil"

class EjercicioBase(BaseModel):
    pregunta: str
    respuesta_correcta: str
    es_multiple_choice: bool = False 
    opciones: Optional[List[str]] = None
    respuesta_correcta: Optional[str] = None
    solucion: Optional[List[str]] = None
    pistas: Optional[List[str]] = None
    concepto_principal: Optional[str] = None
    nivel: NivelEnum

class VIdeosBase(BaseModel):
    url: str
    id: str
    title: str
    thumbnail: str



class SubtemaBase(BaseModel):
    titulo: str
    preguntas: Dict[NivelEnum, List[str]] = {}    
    descripcion: Optional[str] = None
    video_urls: Optional[List[VIdeosBase]] = []
    tema_id: Optional[str] = None
    orden:int

class TemaBase(BaseModel):
    nombre: str
    descripcion: str
    classroom_id:str
    subtema_id: Optional[List[str]] = None
    orden: int = 1

class TemaCreate(TemaBase):
    pass

class SubtemaCreate(SubtemaBase):
    pass

class EjercicioCreate(EjercicioBase):
    pass

class Ejercicio(EjercicioBase):
    id: str = Field( alias="_id")

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class Subtema(SubtemaBase):
    id: str = Field(alias="_id")

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class Tema(TemaBase):
    id: str = Field(alias="_id")

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}