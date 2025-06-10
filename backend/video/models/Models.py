from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime

class Ejercicio(BaseModel):
    enunciado: str
    cuerpo: str     
    opciones: List[str] = []
    respuesta_correcta: str
    dificultad: str  
    explicacion: Optional[str] = None  
    imagen_url: Optional[str] = None   
    tags: List[str] = []             

class TemaBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    profesor_id: int
    video_url: str

class TemaCreate(TemaBase):
    ejercicios: List[Ejercicio] = []

class Tema(TemaBase):
    id: str = Field(alias="_id")
    fecha_creacion: datetime
    ejercicios: List[Ejercicio] = []

    @validator("video_url")
    def validate_youtube_url(cls, v):
        if "youtube.com" not in v and "youtu.be" not in v:
            raise ValueError("URL de YouTube inválida")
        return v