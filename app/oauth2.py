from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta
from .schemas import TokenData
from fastapi.security import OAuth2PasswordBearer
from .database import get_db
from .models import User
from .config import settings

Oauth_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = settings.secret_key
ALGORITH = settings.algorith
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data : dict):
    to_encode = data.copy()
    expire = datetime.utcnow( ) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITH)
    return encoded_jwt

def verify_access_token(token:str, credential_exceptions):
    try:
        payload = jwt.decode(token,SECRET_KEY, algorithms=[ALGORITH])
        id: int = payload.get("user_id")

        if id is None:
            raise credential_exceptions
        token_data = TokenData(id=id)
    except JWTError:
        raise credential_exceptions
    
    return token_data

def verify_user(token:str = Depends(Oauth_scheme), db: Session = Depends(get_db)):
    credential_exceptions = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Login is unauthorized', headers={"WW-Authenticate": "Bearer"})
    token = verify_access_token(token, credential_exceptions)
    user = db.query(User).filter(User.id == token.id).first()
    return user