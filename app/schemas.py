from pydantic import BaseModel, EmailStr
from datetime import datetime

class PostBase(BaseModel):
    title: str
    description: str
    published: bool = True

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    mail: EmailStr
    password:  str
    
class UserRespons(BaseModel):
    id: int
    mail: EmailStr
    created_at:datetime
    
    
    class Config:
        orm_mode = True


class Auth(BaseModel):
    mail: EmailStr
    password: str

