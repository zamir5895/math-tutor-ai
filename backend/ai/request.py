# models/requests.py
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class GenerarEjerciciosRequest(BaseModel):
    tema: str
    forzar_generacion: bool = False

class ResolverEjercicioRequest(BaseModel):
    pregunta: str
    tema: str
    nivel: str = "medio"

class EvaluarRespuestaRequest(BaseModel):
    pregunta: str
    respuesta_correcta: str
    respuesta_alumno: str
    tema: str

class IniciarProgresoRequest(BaseModel):
    alumno_id: str
    tema_id: str

class RegistrarRespuestaRequest(BaseModel):
    progreso_id: str
    nivel: int
    pregunta: str
    respuesta_alumno: str
    respuesta_correcta: str
    tema: str
    tiempo_respuesta: Optional[int] = None

class GenerarReporteRequest(BaseModel):
    alumno_id: str
    tema_id: str

class EjerciciosAdicionalesRequest(BaseModel):
    tema: str
    nivel: str
    cantidad: int = 5
    alumno_id: Optional[str] = None

class AnalisisPatronesRequest(BaseModel):
    alumno_id: str
    tema_id: Optional[str] = None

class LoginAlumnoRequest(BaseModel):
    email: str
    password: str