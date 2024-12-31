
from fastapi import FastAPI
from . import models
from . database import engine
from . routers import post, user, auth, vote

from . config import settings
from fastapi.middleware.cors import CORSMiddleware


   
#models.Base.metadata.create_all(bind=engine)
origins =["https://www.google.com", "https://www.youtube.com"]
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool = True
    # rating: Optional[int] = None



# my_posts = [{"title":"title of the post1", "content":"Content of the post1", "id":1},
#              {"title":"Favorite Foods","content":"I like Pizza","id":2}]

# A method to get a post with a a specific id 
# def find_post(id):
#     for p in my_posts:
#         if p["id"] == id:
#             return p

# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         if p['id']==id:
#             return i
        


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "Welcome to my apii"}

