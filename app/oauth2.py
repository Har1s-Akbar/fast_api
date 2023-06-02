from jose import jwt, JWTError
from datetime import datetime, timedelta

SECRET_KEY = "g2VCVSVT5w9TTfzSzo4MCDZeFtbxVl9k21vHJN1YfUuXF8PJ18xctdCQEjkW"
ALGORITH = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data : dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITH)
    return encoded_jwt