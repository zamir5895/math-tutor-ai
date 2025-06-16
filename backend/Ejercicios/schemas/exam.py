from typing import List, Optional
from pydantic import BaseModel, Field
from bson import ObjectId

from schemas.Util import PyObjectId

class Ejercicio_examen_Base(BaseModel):
    pregunta: str
    respuesta_correcta: str
    es_multiple_choice: bool = False
    opciones: Optional[List[str]] = None
    respuesta: Optional[str] = None
    solucion: Optional[List[str]] = None
    concepto_principal: Optional[str] = None

class Create_Ejercicio_Exaamen(Ejercicio_examen_Base):
    pass

class Ejercicio_examen(Ejercicio_examen_Base):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class Exam_topic_Base(BaseModel):
    """
    Base model for exam topics.
    """

    name: str
    description: str | None = None
    class_room_id: int
    ejercicios: list[Ejercicio_examen] | None = None

class Create_Exam_topic(Exam_topic_Base):
    pass

class Exam_topic(Exam_topic_Base):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}