from pydantic import BaseModel, Field

class EjercicioCreate(BaseModel):
    pregunta: str
    respuesta_correcta: str
    es_multiple_choice: bool = False 
    opciones: list[str] = Field(default_factory=list)
    solucion: list[str] = Field(default_factory=list)
    pistas: list[str] = Field(default_factory=list)
    concepto_principal: str | None = None
    nivel: str 

class EjercicioResueltoCreate(BaseModel):
    alumno_id: str
    salon_id: str
    ejercicio_id: str
    respuesta_usuario: str
class UpdateRespuesta(BaseModel):
    respuesta_usuario:str