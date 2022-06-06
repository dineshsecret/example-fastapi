#swagger documentation url http://127.0.0.1:8000/docs
#redoc documentation url http://127.0.0.1:8000/redoc
#this is my text
# from shutil import ExecError
# from typing import Optional,List
from fastapi import FastAPI #,Body, Depends,Response,status,HTTPException
from fastapi.middleware.cors import CORSMiddleware

# from random import randrange
# import psycopg2 
# from psycopg2.extras import RealDictCursor
# import time
# from requests import Session
#from . import models
#from .database import engine

# from . import utils
from .routers import post,user,auth,vote,welcome
#from  .routers import post,user,auth,vote

from .config import settings
import uvicorn
#models.Base.metadata.create_all(bind=engine) # this line would replace by alembic

app = FastAPI()
origins = ["https://www.google.com","https://www.youtube.com"]
#origins = ["*"] # allow all origines
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(welcome.router)
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

if __name__ == '__main__':
    uvicorn.run(app,host='0.0.0.0',port=8000)
# while True:
#     try:

#         conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='EdgePower2005+',cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("database sonnection was successfull")
#         break
#     except Exception as error:
        
#         print("Connection to database failed")
#         print(error)
#         time.sleep(2)

# my_posts = [{"id":1,"title":"title post1","content":"content post1"},
# {"id":2,"title":"title post2","content":"content post2"}]

# def find_post(id):
#     for p in my_posts:
#         if p['id'] == id:
#             return p

# def find_index_post(id):
#     for i,p in enumerate(my_posts):
#         if p['id'] == id:
#             return i

# @app.get("/")
# async def welcome():
#     return {"message": "Wel come to my API"}


# @app.get("/posts",response_model=List[schemas.Post])
# async def get_posts(db:Session = Depends(get_db)):
#     # cursor.execute("""SELECT * FROM posts """)
#     # posts = cursor.fetchall()
#     posts = db.query(models.Post).all()
#     return posts

# @app.post("/posts",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
# async def create_posts(post:schemas.PostCreate,db:Session = Depends(get_db)):
    
#     new_post = models.Post(**post.dict())
#     db.add(new_post)
#     db.commit()
#     db.refresh(new_post)
#     return new_post


# @app.get("/posts/latest")
# async def get_latest_posts():
#     post = my_posts[len(my_posts)-1]
#     return {"detail":post}

# @app.get("/posts/{id}")
# async def get_post(id:int,db:Session = Depends(get_db)):
    
#     post = db.query(models.Post).filter(models.Post.id == id).first()
#     if not post:
#         raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
#          detail= f"post with id: {id} was not found")
#         # response.status_code = status.HTTP_404_NOT_FOUND
#         # return {"message":f"post with id: {id} was not found"}
#     return post

# @app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
# async def delete_post(id:int,db:Session = Depends(get_db)):
    
#     post = db.query(models.Post).filter(models.Post.id == id)
#     if post.first() == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#          detail=f"post with id {id} does not exists")
#     post.delete(synchronize_session=False)
#     db.commit()
    
#     return Response(status_code=status.HTTP_204_NO_CONTENT)

# @app.put("/posts/{id}",response_model=schemas.Post)
# async def update_post(id:int,updated_post:schemas.PostCreate,db:Session = Depends(get_db)):
#     post_query = db.query(models.Post).filter(models.Post.id == id)

#     post = post_query.first()

#     if post == None:
#         raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
#          detail= f"post with id: {id} was not found")
#     post_query.update(updated_post.dict(),synchronize_session=False)
#     db.commit()
  
#     return post_query.first()

# @app.post("/users",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
# async def create_user(user:schemas.UserCreate, db:Session = Depends(get_db)):

#     #hash passowrd - user.password
#     hashed_password = utils.hash(user.password)
#     user.password = hashed_password
#     new_user = models.User(**user.dict())
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user

# @app.get('/users/{id}',response_model=schemas.UserOut)
# async def get_user(id:int,db:Session = Depends(get_db)):
#     user = db.query(models.User).filter(models.User.id == id).first()
    
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id: {id} does not exist")

#     return user