from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.responses import Response
from ..database import engine, SessionLocal, get_db
from .. import models
from sqlalchemy.orm import Session
from ..schemas import PostCreate, PostResponse
from typing import List, Optional
from ..utils import hash
from ..oauth2 import verify_user

router = APIRouter(
    tags= ['posts'],
)

@router.get("/posts", response_model= List[PostResponse])
def posts(db:Session = Depends(get_db), search:Optional[str] = "", limit: int = 10, skip:int=0, user_cred:int = Depends(verify_user)):
    all_posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return all_posts

@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create(post:PostCreate,db:Session = Depends(get_db), user_cred :int = Depends(verify_user)):
    new_post = models.Post( users_posts_id = user_cred.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    print(user_cred)
    return new_post

@router.get("/posts/{id}", response_model=PostResponse)
def single(id: int, db:Session = Depends(get_db), user_cred :int = Depends(verify_user)):
    print(user_cred.mail)
    one_post = db.query(models.Post).filter(models.Post.id == id).first()
    if one_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with such id des not exist')
    return one_post

@router.delete("/delete/{id}",status_code = status.HTTP_204_NO_CONTENT)
def delete(id: int, db:Session = Depends(get_db), user_cred :int = Depends(verify_user)):
    delete_query = db.query(models.Post).filter(models.Post.id == id)
    delete_post = delete_query.first()
    if delete_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=
        f'post with such id: {id} does not exist')
    if delete_post.users_posts_id != user_cred.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"You are not authorized to delete this post")
    else:
        delete_query.delete(synchronize_session=False)
        db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/update/{id}", response_model=PostResponse)
def edit(id: int, post:PostCreate,db:Session = Depends(get_db), user_cred :int = Depends(verify_user)):
    print(user_cred.id)
    updated_post = db.query(models.Post).filter(models.Post.id == id)
    update = updated_post.first()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with such id: {id} does not exist')
    if update.users_posts_id != user_cred.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"not authorize to edit this post")
    else:
        updated_post.update(post.dict(), synchronize_session=False)
        db.commit()
    return updated_post.first()
    