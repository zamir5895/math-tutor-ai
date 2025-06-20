from pydantic import BaseModel, Field
from typing import Dict
class EjercicioCreate(BaseModel):
    pregunta: str
    respuesta_correcta: str
    es_multiple_choice: bool = False 
    opciones: list[str] = Field(default_factory=list)
    solucion: list[str] = Field(default_factory=list)
    pistas: list[str] = Field(default_factory=list)
    concepto_principal: str | None = None
    nivel: str 

class  EjercicioResueltoCreate(BaseModel):
    alumno_id: str
    salon_id: str
    ejercicio_id: str
    respuesta_usuario: str
    subtema_id: str
class UpdateRespuesta(BaseModel):
    respuesta_usuario:str

class GetEjercicios(BaseModel):
    subtema_id: str
    nivel: str
    alumno_id:str

class EstadisticaCreateRequest(BaseModel):
    alumno_id: str
    tema_id: str
    salon_id: str 
    subtema_id: str
    ejercicios_por_nivel: Dict[str, int] 