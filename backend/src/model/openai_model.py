from pydantic import BaseModel
from typing import List, Dict

class ChatRequest(BaseModel):
    messages: List[Dict]
    api_key: str
    
class ChatResponse(BaseModel):
    message: str