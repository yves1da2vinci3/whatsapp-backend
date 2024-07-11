from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Email(BaseModel):
    email: str

class ModifyUserRequest(BaseModel):
    name: str
    image: str
    
class UserInfo(BaseModel):
    name: Optional[str]
    image: Optional[str]
    createdAt : Optional[datetime]

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    user: dict

class RefreshTokenRequest(BaseModel):
    refresh_token: str
