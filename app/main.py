#swagger documentation url http://127.0.0.1:8000/docs
#redoc documentation url http://127.0.0.1:8000/redoc

import uvicorn
from typing import Optional
from fastapi import Body, FastAPI,Response,status,HTTPException
from pydantic import BaseModel
from random import randrange
import psycopg2 
from psycopg2.extras import RealDictCursor
import time

X:int=0
app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published:bool = True
    rating:Optional[int] = None

while True:
    try:

        conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='EdgePower2005+',cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("database sonnection was successfull")
        break
    except Exception as error:
        
        print("Connection to database failed")
        print(error)
        time.sleep(2)

#my_posts = [{"id":1,"title":"title post1","content":"content post1"},
#{"id":2,"title":"title post2","content":"content post2"}]
my_posts = []



def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.get("/")
async def welcome():
    return {"message": "Wel come to my API"}

@app.get("/posts")
async def get_posts():
    #cursor.execute("""SELECT * FROM posts """)
    #posts = cursor.fetchall()
    return {"data": my_posts}

@app.post("/posts",status_code=status.HTTP_201_CREATED)
async def create_posts(new_post:Post):
    #cursor.execute("""insert into posts (title,content,published) values ({new_post.title},{new_post.content},{new_post.published}) """) # this worked but exporsed to SQL injection
    #cursor.execute("""insert into posts (title,content,published) values (%s,%s,%s) RETURNING * """,(post.title,post.content,post.published))
    #new_post = cursor.fetchone()
    #conn.commit()
    
    post_dict = new_post.dict()
    X=+1
    print(X)
    post_dict['id']=randrange(0,1000000)

    my_posts.append(post_dict)
    return {"data":post_dict}
#title str, content str

@app.get("/posts/latest")
async def get_latest_posts():
    post = my_posts[len(my_posts)-1]
    return {"detail":post}

@app.get("/posts/{id}")
async def get_post(id:int,response: Response):
    #print(type(id))
    #cursor.execute("""SELECT * FROM posts WHERE id = %s """,(str(id)))
    #post = cursor.fetchone()
    # print (test_post)
    #post = find_post(id)
    post = [p for p in my_posts if p['id']==(id)]
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
         detail= f"post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message":f"post with id: {id} was not found"}
    return{"post_detail": post}

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id:int):
    cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING *""",(str(id)))
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
         detail=f"post with id {id} does not exists")
    #index = find_index_post(id)
    # if(index==None):
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #     detail=f"post with id {id} does not exists")
    # my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
async def update_post(id:int,post:Post):
    cursor.execute("""UPDATE posts set title = %s,content=%s,published=%s where id=%s RETURNING *""",(post.title,post.content,post.published,str(id)))
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
         detail= f"post with id: {id} was not found")
    # index = find_index_post(id)
    # if index == None:
    #     raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
    #     detail= f"post with id: {id} was not found")
    # post_dict = post.dict()
    # post_dict['id'] = id
    # my_posts[index] = post_dict
    return {"data":updated_post}

if __name__ == '__main__':
    uvicorn.run(app,host='0.0.0.0',port=8000)