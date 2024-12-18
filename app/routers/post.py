from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from  sqlalchemy.orm import Session
from .. import schemas, models, oauth2
from .. database import get_db
from typing import List

router = APIRouter(
    prefix = "/posts",
    tags = ['Posts']
)

@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return  posts

@router.post("/", status_code= status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post:schemas.PostCreate, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    # """post_dict = new_post.model_dump() # model_dump() converts the type Post in to dictionary.
    # post_dict['id'] = randrange(1,1000000)
    # my_posts.append(post_dict)
    # print(new_post)
    # print(post_dict)"""
    # cursor.execute(""" INSERT INTO posts(title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    print(user_id)
    new_post = models.Post(**post.model_dump())
    print(new_post)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model=schemas.Post)
def get_post(id:int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
   # post = find_post(id)
    # cursor.execute(""" SELECT * FROM posts WHERE id =%s""",(str(id)))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
   
    if not post :
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message": f"post with id: {id} was not found"}
    
    return post

#delete post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING*""",(str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post = db.query(models.Post).filter(models.Post.id == id)
    
   

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post with id : {id} does not exist")
    post.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code = status.HTTP_204_NO_CONTENT)


@router.put("/{id}")
def update_post(id:int, post:schemas.PostCreate, db: Session = Depends(get_db), response_model=schemas.Post, 
                user_id: int = Depends(oauth2.get_current_user)):
    
    # cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",(post.title, post.content, post.published,str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_f = post_query.first()
    print(post)
    if post_f == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail = f"post with id : {id} does not exist")
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()