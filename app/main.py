from fastapi import FastAPI, Response, status, HTTPException#
from fastapi.params import Body
from pydantic import BaseModel

from typing import Optional

import os
from dotenv import load_dotenv

import psycopg2
from psycopg2.extras import RealDictCursor

import time

#Load environment variables from the .env files
load_dotenv()


#Universal language of an API is json, APIs share datas using APIs
app = FastAPI()

class Post(BaseModel):#validates if the input given by the client contains title and content and has the 
                      #datatype assigned to it, this is basically the Schema for the data
    title: str
    content: str
    published: bool = True #If the user doesn't provide a value it is assigned a default value
    #rating: Optional[int] = None #This is a optional field and if the user doesn't give any field input it just assigns it None
while True:
    try:
        conn = psycopg2.connect(
            host=os.getenv("DATABASE_HOST_NAME"),
            database=os.getenv("DATABASE_NAME"),
            user=os.getenv("DATABASE_USERNAME"),
            password=os.getenv("DATABASE_PASSWORD"), # If this is None, you'll get the error above!
            cursor_factory=RealDictCursor
        )

        cursor = conn.cursor()
        print("DataBase connected succesfully.")
        break

    except Exception as error:
        print("Connecttion failed.")
        print("Error: ",error)
        time.sleep(2)


    
cursor.execute("""SELECT * FROM posts """)
my_posts = cursor.fetchall()
#my_posts = [{"title": "title 1", "content": "content 1", "published": True, "rating": 1, "id": 2}]

@app.get("/") #This decorator turns this funtion root into a path operator and get is just an http method
async def root(): #The keyword async is used when we want to perform a asynchronous task
                  #The name of the function doesn't matter it should be relevant though
    return {"message": "Welcome to my api!!!"}

#the path operation that matches is the one thats gonna run
@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts """)
    posts = cursor.fetchall()
    return {"data": posts}

#with post requests we can send data to an API server

#def create_posts(payLoad: dict = Body(...)): #What this does is that it extracts all the fields of the body as dictionary stores it as
                                             #dictionary inside the variable payload
    #print(payLoad)
    #return {"new_post" : f"title: {payLoad['title']} content: {payLoad['content']}"}
@app.post("/posts", status_code=status.HTTP_201_CREATED) #Standard Http request code is set
def create_posts(post: Post): #It stores the data as a pydantic model

    #We dont usually do this because if the user enters any SQL query in the content it could allow
    #the user to essentially manipulate our data and we don't want that
    #cursor.execute(f"INSET INTO posts (title,content,published) VALUES({post.title},{post.content},{post.published})")

    #Here %s is similar to a variable or a placeholder
    cursor.execute("""INSERT INTO posts (title,content, published) VALUES(%s, %s, %s) RETURNING * """,
                   (post.title,post.content,post.published))
    
    new_post = cursor.fetchone()

    conn.commit() #Saving the changes

    return {"data" : new_post}

#We need to be very careful while structuring our API as fastAPI goes through every path parameter till it finds the one its looking for hence order here matters a lot
#FastAPI always works Top-Down
@app.get("/posts/{id}") #here id is a path parameter
def get_post(id: int): #This is used to predefine a variable datatype it tells python that id should be an integer value
    
    #fastAPI automatically extracts the Id
    cursor.execute(""" SELECT * FROM posts WHERE id = %s""",(id,))
    post_found = cursor.fetchone()

    if post_found is None:
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message": f"post with id: {id} not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")
    
    return {"post_detail": post_found}

#deleting posts
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
#Since we have set our status code to 204 no content we would not get any content even it is returned.
def delete_post(id: int):
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """,(id,))
    del_post = cursor.fetchone()
    
    if del_post is None:#when deleting post is not found
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    conn.commit()
    return {"Deleted post": del_post}
    

#updating a post
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,
                     (post.title,post.content,post.published,id))
    upd_post = cursor.fetchone()
    
    if upd_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The post u wanted to update does not exist.")

    conn.commit()
    return {"Updated post": upd_post}
        

#FastAPI does the documentation for your API on its own.