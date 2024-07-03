from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MessageCreate(BaseModel):
    sender: str
    content: str
    type: str  # video, audio, text, file, or image
    timestamp: datetime
    read: Optional[bool] = False
