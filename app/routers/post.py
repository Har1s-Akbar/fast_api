from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.responses import Response
from ..database import engine, SessionLocal, get_db
from .. import models
from sqlalchemy.orm import Session
from ..schemas import PostCreate, PostResponse
from typing import List
from ..utils import hash

router = APIRouter(
    tags= ['posts'],
)

@router.get("/posts", response_model= List[PostResponse])
def posts(db:Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts """)
    # all_posts = cursor.fetchall()
    # print(all_posts)
    all_posts = db.query(models.Post).all()
    return all_posts

@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create(post:PostCreate,db:Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, description,published) VALUES (%s,%s,%s) RETURNING *""", 
    #                (post.title, post.description, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/posts/{id}", response_model=PostResponse)
def single(id: int, db:Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id)))
    # one_post = cursor.fetchone()
    one_post = db.query(models.Post).filter(models.Post.id == id).first()
    if one_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with such id des not exist')
    return one_post

@router.delete("/delete/{id}",status_code = status.HTTP_204_NO_CONTENT)
def delete(id: int, db:Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    # delete_post = cursor.fetchone()
    # conn.commit()
    delete_post = db.query(models.Post).filter(models.Post.id == id)
    if delete_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=
        f'post with such id: {id} does not exist')
    else:
        delete_post.delete(synchronize_session=False)
        db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/update/{id}", response_model=PostResponse)
def update(id: int, post:PostCreate, db:Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title = %s, description= %s, published=%s WHERE id = %s RETURNING *""",
    #                (post.title, post.description, post.published, str(id)))
    # updated_Post = cursor.fetchone()
    # conn.commit()
    updated_post = db.query(models.Post).filter(models.Post.id == id)
    updated_post.first()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with such id: {id} does not exist')
    else:
        updated_post.update(post.dict(), synchronize_session=False)
        db.commit()
    return updated_post.first()
