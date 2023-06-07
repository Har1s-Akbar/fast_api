from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .database import engine, SessionLocal, get_db
from . import models
from .routers import post, user, auth, votes

app = FastAPI()
models.Base.metadata.create_all(bind= engine)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(votes.router)