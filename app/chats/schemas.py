from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ChatBase(BaseModel):
    name: str
    image: Optional[str] = None
    created_time: datetime
    type: str
    admin_id: int

class ChatCreate(ChatBase):
    participants: List[int]

class ChatUpdate(BaseModel):
    name: Optional[str] = None
    image: Optional[str] = None

class ChatResponse(ChatBase):
    id: int
    participants: List[int]

    class Config:
        orm_mode = True

class MessageBase(BaseModel):
    content: str
    type: str

class MessageCreate(MessageBase):
    user_id: int
    chat_id: int

class MessageResponse(MessageBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
