from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class StoryBase(BaseModel):
    type: str
    user_id: int

class StoryCreate(StoryBase):
    content: str

class StoryResponse(StoryBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
