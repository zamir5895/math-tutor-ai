from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from bson import ObjectId
from alumno import PyObjectId

class MetricasDetalladas(BaseModel):
    precision_por_nivel: Dict[str, float] = {}
    tiempo_promedio_respuesta: Optional[float] = None
    conceptos_dominados: List[str] = []
    conceptos_a_reforzar: List[str] = []
    progresion_temporal: List[Dict[str, Any]] = []

class ReporteBase(BaseModel):
    alumno_id: PyObjectId
    tema_id: PyObjectId
    tema_nombre: str
    nivel_maximo: int
    respuestas_totales: int
    correctas: int
    porcentaje: float
    observaciones: str
    metricas_detalladas: Optional[MetricasDetalladas] = None
    recomendaciones: List[str] = []
    fecha: datetime = Field(default_factory=datetime.utcnow)

class ReporteCreate(ReporteBase):
    pass

class Reporte(ReporteBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
