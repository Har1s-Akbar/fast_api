from fastapi import APIRouter,status, HTTPException, Depends
from ..database import get_db
from .. import models
from sqlalchemy.orm import Session
from ..schemas import UserCreate, UserRespons
from ..utils import hash

router = APIRouter(
    tags=['user'],
)

@router.post("/user", status_code=status.HTTP_201_CREATED, response_model=UserRespons)
def create(user:UserCreate ,db:Session = Depends(get_db)):
    hash_password = hash(user.password)
    user.password = hash_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/user/{id}", response_model=UserRespons)
def find(id:int ,db:Session = Depends(get_db)):
    find_post = db.query(models.User).filter(models.User.id == id).first()
    if find_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with such id {id} does not exist")
    
    return find_post