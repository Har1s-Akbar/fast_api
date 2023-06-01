from fastapi import FastAPI, status, HTTPException, Depends
from pydantic import BaseModel
from fastapi.responses import Response
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .database import engine, SessionLocal, get_db
from . import models
from sqlalchemy.orm import Session

app = FastAPI()

class Post(BaseModel):
    title: str
    description: str
    published: bool = True

models.Base.metadata.create_all(bind= engine)

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='admin', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Database succesfully connected')
        break
    except Exception as error:
        print('connection failed')
        print('error:', error)
        time.sleep(3)


@app.get("/posts")
def posts():
    cursor.execute("""SELECT * FROM posts """)
    all_posts = cursor.fetchall()
    print(all_posts)
    return {'all': all_posts}

@app.get("/alchemy")
def alchemy(db:Session = Depends(get_db)):
    return {'status': 'working'}

@app.post("/create", status_code=status.HTTP_201_CREATED)
def create(post:Post):
    cursor.execute("""INSERT INTO posts (title, description,published) VALUES (%s,%s,%s) RETURNING *""", 
                   (post.title, post.description, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}

@app.get("/posts/{id}")
def single(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id)))
    one_post = cursor.fetchone()
    if one_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with such id des not exist')
    return {'post' : one_post}

@app.delete("/delete/{id}",status_code = status.HTTP_204_NO_CONTENT)
def delete(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    delete_post = cursor.fetchone()
    conn.commit()
    if delete_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with such id: {id} does not exist')
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/update/{id}")
def update(id: int, post:Post):
    cursor.execute("""UPDATE posts SET title = %s, description= %s, published=%s WHERE id = %s RETURNING *""",
                   (post.title, post.description, post.published, str(id)))
    updated_Post = cursor.fetchone()
    conn.commit()
    if updated_Post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with such id: {id} does not exist')
    return {'message' : updated_Post}