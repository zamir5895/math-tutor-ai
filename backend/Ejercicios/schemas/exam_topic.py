from typing import List, Optional
from pydantic import BaseModel, Field
from bson import ObjectId
from Temas import Ejercicio
from schemas.Util import PyObjectId


class Exam_topic_Base(BaseModel):
    """
    Base model for exam topics.
    """

    name: str
    description: str | None = None
    topic_id: Optional[PyObjectId] = None
    class_room_id: int
    ejercicios: list[Ejercicio] = []

class Exam_topic(Exam_topic_Base):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}