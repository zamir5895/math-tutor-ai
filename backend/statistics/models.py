from pydantic import BaseModel
from typing import Dict

class EstadisticaCreateRequest(BaseModel):
    alumno_id: str
    tema_id: str
    salon_id: str 
    subtema_id: str
    ejercicios_por_nivel: Dict[str, int] 

class ProgresoEvent(BaseModel):
    alumno_id: str
    tema_id: str
    subtema_id: str
    nivel: str
    es_correcto: bool