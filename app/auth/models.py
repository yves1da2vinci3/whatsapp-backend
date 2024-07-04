from pydantic import BaseModel

class User(BaseModel):
    email: str
    name: str = None
    image: str = None
