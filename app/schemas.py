from pydantic import BaseModel, EmailStr, conint, ConfigDict
from datetime import datetime
from typing import Union, Optional, Literal, Dict, Tuple
class PostBase(BaseModel):
    title: str
    content: str
    published: Optional[bool] = None

    

class PostCreate(PostBase):
    pass


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    
# response
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    
class PostOut(Post):
    Post: Post
    votes: int  
    class Config:
        orm_mode = True

# Creating user schema
class UserCreate(BaseModel):
    email: EmailStr
    password: str

    

class UserLogin(BaseModel):
    email: EmailStr
    password: str

    

class Token(BaseModel):
    access_token: str
    token_type: str

    

class TokenData(BaseModel):
    id:Union[int, None] = None
    # Use ConfigDict for ORM validation
    

class Vote(BaseModel):
    post_id: int
    dir: Literal[0, 1]
    # Use ConfigDict for ORM validation
    