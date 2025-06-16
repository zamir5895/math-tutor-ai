from pydantic import BaseModel, Field
from typing import List, Optional, Union
from datetime import datetime

class MultipleChoiceAnswer(BaseModel):
    option: str 
    text: str

class Exercise(BaseModel):
    tema: str
    problema: str
    is_multiple_choice: bool
    respuestas: Optional[List[MultipleChoiceAnswer]] = None  
    respuesta_correcta: Union[str, List[str]]  
    tiene_imagen: bool = False
    imagen_url: Optional[str] = None  
    imagen_descripcion: Optional[str] = None  
    created_at: datetime = Field(default_factory=datetime.now)

class ExerciseResponse(BaseModel):
    id: str
    tema: str
    problema: str
    is_multiple_choice: bool
    respuestas: Optional[List[MultipleChoiceAnswer]] = None
    respuesta_correcta: Union[str, List[str]]
    tiene_imagen: bool = False
    imagen_url: Optional[str] = None
    imagen_descripcion: Optional[str] = None
    created_at: datetime

class ProcessPDFResponse(BaseModel):
    message: str
    total_exercises: int
    exercises_ids: List[str]