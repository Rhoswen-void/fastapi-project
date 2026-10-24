from fastapi import FastAPI, Response, status, HTTPException#
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

#Universal language of an API is json, APIs share datas using APIs
app = FastAPI()

class Post(BaseModel):#validates if the input given by the client contains title and content and has the 
                      #datatype assigned to it, this is basically the Schema for the data
    title: str
    content: str
    published: bool = True #If the user doesn't provide a value it is assigned a default value
    rating: Optional[int] = None #This is a optional field and if the user doesn't give any field input it just assigns it None

def find_posts(id: int): #This is used to get a post the post info and is a python function
    for post in my_posts:
        if post['id'] == id:
            return post
    return None

#function to find if post with the given id exists or not
def find_id(id: int):
    for post in my_posts:
        if post['id'] == id:
            return my_posts.index(post)
    return None
    

my_posts = [{"title": "title 1", "content": "content 1", "published": True, "rating": 1, "id": 2}]

@app.get("/") #This decorator turns this funtion root into a path operator and get is just an http method
async def root(): #The keyword async is used when we want to perform a asynchronous task
                  #The name of the function doesn't matter it should be relevant though
    return {"message": "Welcome to my api!!!"}

#the path operation that matches is the one thats gonna run
@app.get("/posts")
def get_posts():
    return {"data": my_posts}

#with post requests we can send data to an API server

#def create_posts(payLoad: dict = Body(...)): #What this does is that it extracts all the fields of the body as dictionary stores it as
                                             #dictionary inside the variable payload
    #print(payLoad)
    #return {"new_post" : f"title: {payLoad['title']} content: {payLoad['content']}"}
@app.post("/posts", status_code=status.HTTP_201_CREATED) #Standard Http request code is set
def create_posts(post: Post): #It stores the data as a pydantic model
    post_dict = post.model_dump()
    post_dict['id'] = randrange(0,10000000) #Randomly generates an Id for the post
    my_posts.append(post_dict)
    return {"data" : post_dict}

#We need to be very careful while structuring our API as fastAPI goes through every path parameter till it finds the one its looking for hence order here matters a lot
#FastAPI always works Top-Down
@app.get("/posts/{id}") #here id is a path parameter
def get_post(id: int): #This is used to predefine a variable datatype it tells python that id should be an integer value

    #fastAPI automatically extracts the Id
    post_found = find_posts(id) 
    if not post_found:
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message": f"post with id: {id} not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")
    return {"post_detail": post_found}

#deleting posts
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    flag = False 
    for post in my_posts: #This loop is used to find the post that we want to delete
        if post['id'] == id:
            flag = True
            my_posts.pop(my_posts.index(post))
            return {"message": f"Post with id: {id} has been deleted."}
            

    if not flag: #If the post to be deleted is not found
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")


#updating a post
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_id(id)

    if index != None:
        post_dict = post.model_dump() #Converting the the post into a normal python dictionary
        post_dict['id'] = id
        my_posts[index] = post_dict
        return {"message": "Updated post."}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The post u wanted to update does not exist.")
        

#FastAPI does the documentation for your API on its own.