from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.enums import ChatType, MessageType

class ChatCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    image: Optional[str] = None
    type: ChatType

class ChatUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    image: Optional[str] = None

class MessageCreate(BaseModel):
    content: str
    type: MessageType

class MessageResponse(BaseModel):
    id: int
    content: str
    type: MessageType
    chat_id: int
    user_id: int
    created_time: datetime

    class Config:
        from_attributes = True

class ChatResponse(BaseModel):
    id: int
    name: str
    image: Optional[str]
    created_time: datetime
    type: ChatType
    admin_id: int
    last_message: Optional[MessageResponse]

    class Config:
        from_attributes = True