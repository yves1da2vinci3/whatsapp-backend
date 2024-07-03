from pydantic import BaseModel

class PhoneNumber(BaseModel):
    number: str

class UserInfo(BaseModel):
    name: str
    image: str
