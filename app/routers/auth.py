from fastapi import APIRouter, Depends, status,HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import Token
from ..models import User
from ..utils import hash_verify
from ..oauth2 import create_access_token

router = APIRouter()

@router.post('/login')
def auth(credentials: OAuth2PasswordRequestForm = Depends() ,db: Session = Depends(get_db)):
    
    user = db.query(User).filter(User.mail == credentials.username).first()
    if not user :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="invalid credentials")
    
    if not hash_verify(credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="invalid credentials")
    
    access_token = create_access_token({"user_id": user.id})
    return {'access_token': access_token, 'token_type':'bearer token'}