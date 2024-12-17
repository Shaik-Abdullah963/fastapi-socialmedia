from pydantic import BaseModel
from datetime import datetime
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