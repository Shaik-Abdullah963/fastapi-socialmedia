from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
import json
from  sqlalchemy.orm import Session, aliased
from sqlalchemy import func
from .. import schemas, models, oauth2
from .. database import get_db
from typing import List, Optional, Tuple, Dict, Union
from fastapi.encoders import jsonable_encoder

router = APIRouter(
    prefix = "/posts",
    tags = ['Posts']
)
#@router.get("/", response_model=List[tuple(schemas.PostOut.values())])
#r = {"post": item[0] for item in List[Tuple[schemas.Post, int]]}
#@router.get("/", response_model=List[Tuple[schemas.Post, int]]) 
@router.get("/", response_model=List[Dict[str, Union[schemas.Post, int]]])
def get_posts(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
    limit: int = 10, skip: int = 0, search: Optional[str] = ""):
 

    # models.User = Depends(oauth2.get_current_user) this line fetches user information for every path operation. 
    #It is not neccessary to do so.

    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
 
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True
    ).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    
    # Convert the results into a list of dictionaries
    
    # Convert the query results into a list of PostOut schema objects
    
    
    
    serialized_results = []
    for post, votes in results:
        serialized_post = {
            "post": {
                "id": post.id,
                "title": post.title,
                "content": post.content,
                "published": post.published,
                "created_at": post.created_at,
                "owner_id": post.owner_id,
                "owner": {
                    "id": post.owner.id,
                    "email": post.owner.email,
                    "created_at": post.owner.created_at
                },
            },
            "votes": votes,
        }
        serialized_results.append(serialized_post)

    return serialized_results
    
    
    

@router.post("/", status_code= status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post:schemas.PostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    # models.User = Depends(oauth2.get_current_user) this line fetches user information for every path operation. 
    #It is not neccessary to do so.

    # """post_dict = new_post.model_dump() # model_dump() converts the type Post in to dictionary.
    # post_dict['id'] = randrange(1,1000000)
    # my_posts.append(post_dict)
    # print(new_post)
    # print(post_dict)"""
    # cursor.execute(""" INSERT INTO posts(title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    print(current_user.id)
    new_post = models.Post(owner_id = current_user.id, **post.model_dump())
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}")
def get_post(id:int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    # models.User = Depends(oauth2.get_current_user) this line fetches user information for every path operation. 
    #It is not neccessary to do so.
   # post = find_post(id)
    # cursor.execute(""" SELECT * FROM posts WHERE id =%s""",(str(id)))
    # post = cursor.fetchone()
    
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True
    ).group_by(models.Post.id).filter(models.Post.id == id).first()
   
    if not post :
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message": f"post with id: {id} was not found"}
    
    post, votes = post
    
    serialized_post = {
            "post": {
                "id": post.id,
                "title": post.title,
                "content": post.content,
                "published": post.published,
                "created_at": post.created_at,
                "owner_id": post.owner_id,
                "owner": {
                    "id": post.owner.id,
                    "email": post.owner.email,
                    "created_at": post.owner.created_at
                },
            },
            "votes": votes,
    }
    
    return serialized_post

#delete post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    # models.User = Depends(oauth2.get_current_user) this line fetches user information for every path operation. 
    #It is not neccessary to do so.

    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING*""",(str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
     
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id : {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not the owner of this post")
    post_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code = status.HTTP_204_NO_CONTENT)


@router.put("/{id}")
def update_post(id:int, updated_post:schemas.PostCreate, db: Session = Depends(get_db), response_model=schemas.Post, 
                current_user: models.User = Depends(oauth2.get_current_user)):
    
    # models.User = Depends(oauth2.get_current_user) this line fetches user information for every path operation. 
    #It is not neccessary to do so.

    # cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",(post.title, post.content, post.published,str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail = f"post with id : {id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not the owner of this post")
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()