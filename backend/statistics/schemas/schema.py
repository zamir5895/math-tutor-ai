
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from typing import Optional
from schemas.util import PyObjectId
class NivelEnum(str, Enum):
    facil = "facil"
    medio = "medio"
    dificil = "dificil"


class statsPorEejercicioBaseParaProfesor(BaseModel):
    ejercicio_id:str
    cantidad_alumnos:int=0
    cantidad_resolvieron:int=0
    cantidad_no_resolvieron:int=0
    cantidad_correctos:int=0
    cantidad_incorrectos:int=0
    porcentaje_correctos:float=0.0
    porcentaje_incorrectos:float=0.0

class statsPorSubtemaBaseParaProfesor(BaseModel):
    subtema_id:str
    tema_id:str
    cantidad_alumnos:int=0
    cantidad_ejercicios:int=0
    cantidad_resolvieron:int=0
    cantidad_no_resolvieron:int=0
    cantidad_correctos:int=0
    cantidad_incorrectos:int=0
    porcentaje_correctos:float=0.0
    porcentaje_incorrectos:float=0.0    
    porcentaje_avanze:float=0.0

class StatsPorNivelSubtemaBaseParaProfesor(BaseModel):
    subtema_id:str
    tema_id:str
    nivel:NivelEnum
    cantidad_alumnos:int=0
    cantidad_ejercicios:int=0
    cantidad_resolvieron:int=0
    cantidad_no_resolvieron:int=0
    cantidad_correctos:int=0
    cantidad_incorrectos:int=0
    porcentaje_correctos:float=0.0
    porcentaje_incorrectos:float=0.0    
    porcentaje_avanze:float=0.0

class statsPorTemaBaseParaProfesor(BaseModel):
    tema_id:str
    cantidad_alumnos:int=0
    cantidad_subtemas:int=0
    porcentaje_avanze:float=0.0
    cantidad_ejercicios:int=0

class statsPorSalonBaseParaProfesor(BaseModel):
    salon_id:str
    porcentaje_avanze:float=0.0

class statsPorAlumnoBaseParaProfesor(BaseModel):
    salon_id:str
    alumno_id:str
    cantidad_ejercicios_resueltos:int=0
    cantidad_ejercicios_no_resueltos:int=0
    porcentaje_avanze:float=0.0
    cantidad_ejercicios_correctos:int=0
    cantidad_ejercicios_incorrectos:int=0
    porcentaje_correctos:float=0.0
    porcentaje_incorrectos:float=0.0
    porcentaje_precision:float=0.0

class StatsPorNivel(BaseModel):
    cantidad_ejercicios: int = 0
    cantidad_ejercicios_resueltos: int = 0
    cantidad_ejercicios_no_resueltos: int = 0
    porcentaje_avanze: float = 0.0
    cantidad_ejercicios_correctos: int = 0
    cantidad_ejercicios_incorrectos: int = 0


class statsPorNivelSubtemaBaseParaAlumno(BaseModel):
    alumno_id:str
    tema_id:str
    subtema_id:str
    facil: StatsPorNivel = StatsPorNivel()
    medio: StatsPorNivel = StatsPorNivel()  
    dificil: StatsPorNivel = StatsPorNivel()

    

class statsSubtemaBaseParaAlumno(BaseModel):
    alumno_id:str
    subtema_id:str
    tema_id:str
    cantidad_ejercicios:int=0
    cantidad_ejercicios_resueltos:int=0
    cantidad_ejercicios_no_resueltos:int=0
    porcentaje_avanze:float=0.0
    cantidad_ejercicios_correctos:int=0
    cantidad_ejercicios_incorrectos:int=0
    porcentaje_correctos:float=0.0
    porcentaje_incorrectos:float=0.0
    porcentaje_precision:float=0.0

class statsTemaBaseParaAlumno(BaseModel):
    alumno_id:str
    tema_id:str
    cantidad_subtemas:int=0
    cantidad_subtemas_terminados:int=0
    porcentaje_avanze:float=0.0
class HistorialProgreso(BaseModel):
    fecha: datetime
    progreso: float= 0.0

class UltimoEjercicio(BaseModel):
    ejercicio_id: str
    fecha: datetime
    resultado: str  

class statsAlumnoBase(BaseModel):
    alumno_id: str
    salon_id: str
    progreso_general: float = 0.0
    historial_progreso: List[HistorialProgreso] = []
    errores_comunes: List[str] = []
    tiempo_total: int = 0  
    ultimos_ejercicios: List[UltimoEjercicio] = []
    racha_actual: int = 0
    fecha_ultima_actividad: datetime = datetime.now()


class statsPorEejercicioCreateParaProfesor(statsPorEejercicioBaseParaProfesor):
    pass
class statsPorSubtemaCreateParaProfesor(statsPorSubtemaBaseParaProfesor):
    pass

class statsPorNivelSubtemaCreateParaProfesor(StatsPorNivelSubtemaBaseParaProfesor):
    pass

class statsPorTemaCreateParaProfesor(statsPorTemaBaseParaProfesor):
    pass
class statsPorSalonCreateParaProfesor(statsPorSalonBaseParaProfesor):
    pass   
class statsPorAlumnoCreateParaProfesor(statsPorAlumnoBaseParaProfesor):
    pass
class statsPorNivelSubtemaCreateParaAlumno(statsPorNivelSubtemaBaseParaAlumno):
    pass
class statsSubtemaCreateParaAlumno(statsSubtemaBaseParaAlumno):
    pass
class statsTemaCreateParaAlumno(statsTemaBaseParaAlumno):
    pass
class statsAlumnoCreate(statsAlumnoBase):
    pass
class statsPorEejercicioParaProfesor(statsPorEejercicioBaseParaProfesor):
    id: str = Field(alias="_id")

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class statsPorSubtemaParaProfesor(statsPorSubtemaBaseParaProfesor):
    id: str = Field(alias="_id")

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class statsPorNivelSubtemaParaProfesor(StatsPorNivelSubtemaBaseParaProfesor):
    id: str = Field(alias="_id")

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class statsPorTemaParaProfesor(statsPorTemaBaseParaProfesor):
    id: str = Field(alias="_id")

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class statsPorSalon(statsPorSalonBaseParaProfesor):
    id: str = Field(alias="_id")

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
class statsPorAlumnoParaProfesor(statsPorAlumnoBaseParaProfesor):
    id: str = Field(alias="_id")

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class statsPorNivelSubtemaAlumno(statsPorNivelSubtemaBaseParaAlumno):
    id: str = Field(alias="_id")

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
class statsSubtemaAlumno(statsSubtemaBaseParaAlumno):
    id: str = Field(alias="_id")

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
class statsTemaAlumno(statsTemaBaseParaAlumno):
    id: str = Field(alias="_id")

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
class statsAlumno(statsAlumnoBase):
    id: str = Field(alias="_id")

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
