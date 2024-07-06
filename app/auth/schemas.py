from pydantic import BaseModel

class Email(BaseModel):
    email: str

class UserInfo(BaseModel):
    name: str
    image: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    user: dict

class RefreshTokenRequest(BaseModel):
    refresh_token: str
