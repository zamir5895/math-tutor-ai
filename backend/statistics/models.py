from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class EstadisticasGenerales(BaseModel):
    total_alumnos: int
    total_profesores: int
    total_salones: int
    usuarios_por_rol: dict

class ProgresoEstadistica(BaseModel):
    alumno_id: str
    nivel_promedio: float
    porcentaje_aciertos: float
    ejercicios_resueltos: int

class ReporteEstadistica(BaseModel):
    alumno_id: str
    promedio_porcentaje: float
    nivel_maximo_promedio: float

class DificultadConcepto(BaseModel):
    concepto: str
    frecuencia: int

class EstadisticasProfesor(BaseModel):
    profesor_id: str
    promedio_alumnos_por_salon: float
    rendimiento_promedio: float

class SalonResumen(BaseModel):
    salon_id: str
    total_alumnos: int
    promedio_rendimiento: float
