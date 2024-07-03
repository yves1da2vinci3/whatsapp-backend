from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class Call(BaseModel):
    caller: str
    receiver: str
    type: str  # audio or video
    timestamp: datetime
    duration: Optional[int] = None
    participants: List[str]
