from typing import List, Optional
from pydantic import BaseModel, Field
from bson import ObjectId
from enum import Enum 
from schemas.Util import PyObjectId

class PDFBase(BaseModel):
    url: str
    class_roomd_id:int
class PDFCreate(PDFBase):
    pass
class PDF(PDFBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}