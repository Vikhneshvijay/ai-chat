from pydantic import BaseModel
from typing import List, Optional

class ChatRequest(BaseModel):
    session_id: str
    message: str

class ChatResponse(BaseModel):
    session_id: str
    user_message: str
    ai_response: str
    timestamp: str

class Message(BaseModel):
    role: str
    content: str
    created_at: str

class ChatHistory(BaseModel):
    session_id: str
    messages: List[Message]

class HealthStatus(BaseModel):
    status: str
    ollama: str

class ModelList(BaseModel):
    models: Optional[List[dict]] = None
