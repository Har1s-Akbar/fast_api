from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional


class UserRespons(BaseModel):
    id: int
    mail: EmailStr
    created_at:datetime
    
    
    class Config:
        orm_mode = True


class PostBase(BaseModel):
    title: str
    description: str
    published: bool = True
    
class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created_at: datetime
    users_posts_id : str
    user:UserRespons


    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    mail: EmailStr
    password:  str
    
class Auth(BaseModel):
    mail: EmailStr
    password: str

class Token(BaseModel):
    accesstoken = str
    token_type = str

class TokenData(BaseModel):
    id: Optional[str]

class VoteCreate(BaseModel):
    post_id : int
    dir: conint(le=1)