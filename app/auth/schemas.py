from pydantic import BaseModel

class Email(BaseModel):
    email: str

class UserInfo(BaseModel):
    name: str
    image: str
