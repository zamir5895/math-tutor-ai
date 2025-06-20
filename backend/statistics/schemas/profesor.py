from typing import List, Dict
from pydantic import BaseModel
from datetime import datetime
from enum import Enum

from schemas.alumno import NivelDificultad, ProgresoBase, DesempenoNivel
class DesempenoGrupo(BaseModel):
    promedio: float
    mejor: float
    peor: float

class EjercicioProblematico(BaseModel):
    id: str
    nombre: str
    porcentaje_error: float
    alumnos_con_dificultad: List[str]  

class SubtemaProfesor(BaseModel):
    id: str
    nombre: str
    progreso_grupo: ProgresoBase
    niveles: Dict[NivelDificultad, DesempenoGrupo]
    ejercicios_problematicos: List[EjercicioProblematico]
    alumnos_rezagados: List[str]  

class TemaProfesor(BaseModel):
    id: str
    nombre: str
    progreso_grupo: ProgresoBase
    subtemas: List[SubtemaProfesor]

class AlumnoResumen(BaseModel):
    id: str
    nombre: str
    avatar: str  
    progreso: float

class EstadisticasSalonResponse(BaseModel):
    salon_id: str
    nombre_salon: str
    temas: List[TemaProfesor]
    alumnos: List[AlumnoResumen]  
    promedio_general: float
    alumnos_destacados: List[str] 