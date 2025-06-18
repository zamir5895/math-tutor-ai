from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class UserMessage(BaseModel):
    user_id: str
    conversation_id: Optional[str] = None
    message: str

class AIResponse(BaseModel):
    conversation_id: str
    response: str
    context_used: List[str]

class Conversation(BaseModel):
    user_id: str
    conversation_id: str
    messages: List[dict]
    created_at: datetime
    updated_at: datetime