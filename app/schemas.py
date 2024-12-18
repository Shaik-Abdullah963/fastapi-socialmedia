from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Union
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
class PostCreate(PostBase):
    pass

# response
class Post(PostBase):
    id: int
    created_at: datetime
    # the field title, content and published are inherited from the PostBase class

# Creating user schema
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    # class Config:
    #     orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id:Union[int, None] = None