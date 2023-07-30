from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional


class Post(BaseModel):
    title :str
    content: str
    published: bool = True
    id: int
    rating: Optional[int] =None


app = FastAPI()

@app.get("/")
def root():
    return {"message":"Welcome to my API"}

@app.get("/posts")
def get_posts():
    return {"message": "These are my posts"}

@app.post("/createposts")
def create_posts(post: Post):
    print (post)
    print (post.model_dump())
    return {"New post":post}