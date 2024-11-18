from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

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
        

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Welcome to my apii"}
@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts """)
    posts = cursor.fetchall()
    print(posts)
    print(type(posts))
    return {"data": posts}

@app.post("/posts", status_code= status.HTTP_201_CREATED)
def create_posts(post: Post):
    """post_dict = new_post.model_dump() # model_dump() converts the type Post in to dictionary.
    post_dict['id'] = randrange(1,1000000)
    my_posts.append(post_dict)
    print(new_post)
    print(post_dict)"""
    cursor.execute(""" INSERT INTO posts(title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}

@app.get("/posts/{id}")
def get_post(id:int, response: Response):
   # post = find_post(id)
    cursor.execute(""" SELECT * FROM posts WHERE id =%s""",(str(id)))
    post = cursor.fetchone()
    print(post)
   
    if not post :
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message": f"post with id: {id} was not found"}
    
    return {"post_detail":post}

#delete post

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post with id : {id} does not exist")
    my_posts.pop(index)
    return Response(status_code = status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id:int, post:Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail = f"post with id : {id} does not exist")
    post_dict = post.model_dump()
    post_dict['id'] = id
    my_posts[index]= post_dict
    return {"data":post_dict}