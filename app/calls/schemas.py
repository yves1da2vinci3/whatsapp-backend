from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class CallCreate(BaseModel):
    caller: str
    receiver: str
    type: str  # audio or video
    timestamp: datetime
    duration: Optional[int] = None
    participants: List[str]
