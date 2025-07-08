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
    title: str
    messages: List[dict]
    created_at: datetime
    updated_at: datetime

class ConversationSummary(BaseModel):
    id: str
    title: str
    last_message: str
    updated_at: str