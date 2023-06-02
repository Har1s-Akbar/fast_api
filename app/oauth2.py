from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from datetime import datetime, timedelta
from .schemas import TokenData
from fastapi.security import OAuth2PasswordBearer

Oauth_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = "g2VCVSVT5w9TTfzSzo4MCDZeFtbxVl9k21vHJN1YfUuXF8PJ18xctdCQEjkW"
ALGORITH = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data : dict):
    to_encode = data.copy()
    expire = datetime.utcnow( ) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITH)
    return encoded_jwt

def verify_access_token(token:str, credential_exceptions):
    try:
        payload = jwt.decode(token,SECRET_KEY, algorithms=[ALGORITH])
        id: str = payload.get("user_id")

        if id is None:
            raise credential_exceptions
        token_data = TokenData(id=id)

        return token_data
    except JWTError:
        raise credential_exceptions
    
    return token_data

def verify_user(token:str = Depends(Oauth_scheme)):
    credential_exceptions = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Login is unauthorized', headers={"WW-Authenticate": "Bearer"})

    return verify_access_token(token, credential_exceptions)