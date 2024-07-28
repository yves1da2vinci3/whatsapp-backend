from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
from app.enums import ChatType, MessageType
from app.auth.models import User


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    image: str

    class Config:
        arbitrary_types_allowed = True


class ChatCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    image: Optional[str] = None
    type: ChatType
    participants_ids: List[int]


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
    participants: List[UserResponse]
    created_time: datetime
    type: ChatType
    admin_id: int
    last_message: Optional[MessageResponse]

    class Config:
        from_attributes = True


def user_to_user_response(user: User) -> UserResponse:
    return UserResponse(id=user.id, email=user.email, name=user.name, image=user.image)
