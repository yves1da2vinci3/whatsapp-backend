from pydantic import BaseModel
from typing import List
from datetime import datetime

class Message(BaseModel):
    sender: str
    content: str
    type: str  # video, audio, text, file, or image
    timestamp: datetime
    read: bool = False

class Chat(BaseModel):
    participants: List[str]
    messages: List[Message]
