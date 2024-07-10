from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CallCreate(BaseModel):
    caller_id: int
    receiver_id: int
    duration: int
    called_at: datetime

class CallUpdate(BaseModel):
    duration: Optional[int] = None
    called_at: Optional[datetime] = None

class CallResponse(BaseModel):
    id: int
    caller_id: int
    receiver_id: int
    duration: int
    called_at: datetime

    class Config:
        orm_mode = True
