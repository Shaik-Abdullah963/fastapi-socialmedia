from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel

from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from  sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, SessionLocal, get_db
from .routers import post, user
   
models.Base.metadata.create_all(bind=engine)

app = FastAPI()



# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool = True
    # rating: Optional[int] = None

while True:
    try:
        conn = psycopg2.connect(host = 'localhost', database = 'fastapi', user = 'postgres', password = 'Asif@09060456', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database Connecion was Successful")
        break
    except Exception as error:
        print("Connection to database failed")
        print("Error: ",error)
        time.sleep(2)

my_posts = [{"title":"title of the post1", "content":"Content of the post1", "id":1},
             {"title":"Favorite Foods","content":"I like Pizza","id":2}]

# A method to get a post with a a specific id 
def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id']==id:
            return i
        


app.include_router(post.router)
app.include_router(user.router)

@app.get("/")
def root():
    return {"message": "Welcome to my apii"}

