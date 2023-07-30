from fastapi import FastAPI, Response,status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange


class Post(BaseModel):
    title :str
    content: str
    published: bool = True
    rating: Optional[int] =None

my_posts = [{"travel":"Best location", "content":"Welcome to saint Tropez", "id":1},
            {"title":"Good food", "content":"I like pizza", "id":2}]

def find_post(id):
    try:
        for p in my_posts:
            if p['id'] == id:
                return p
    except Exception as e:
        print (f"Unexpected error occured: {e}")

def find_post_index(id):
    try:
        for i, p in enumerate(my_posts):
            if p['id'] == id:
                return i
    except Exception as e:
        print (f"Unexpected error occured: {e}")


app = FastAPI()

@app.get("/")
def root():
    return {"message":"Welcome to my API"}

@app.get("/posts")
def get_posts():
    return {"message": my_posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict=post.model_dump()
    post_dict['id']=randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"New post":post_dict}

@app.get("/posts/{id}")
def get_post(id : int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id of {id} was not found")
    return{"post":post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Post with id of {id} was not found")

    my_posts.remove(post)
    return Response(status_code=status.HTTP_204_NO_CONTENT) # when deleting a message, no content can be sent

@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id : int, post : Post):
    index = find_post_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Post with id of {id} was not found")
    post_dict = post.model_dump()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"Updqted": f"Post with id of {id} has been updated with {post_dict}"}