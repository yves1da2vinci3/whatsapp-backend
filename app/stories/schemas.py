from pydantic import BaseModel
from datetime import datetime

class StoryCreate(BaseModel):
    user_id: str
    content: str
    type: str  # image, video, text
    timestamp: datetime
