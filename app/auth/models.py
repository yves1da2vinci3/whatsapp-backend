from pydantic import BaseModel

class User(BaseModel):
    phone: str
    name: str = None
    image: str = None
