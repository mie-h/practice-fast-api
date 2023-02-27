from fastapi import FastAPI, status, HTTPException, Response
from pydantic import BaseModel


app = FastAPI()


class Post(BaseModel):
    id: int
    title: str


my_posts = [{"id": 1, "title":"title1"}, {"id": 2, "title":"title2"}]


def find_post(id):
    for i, post in enumerate(my_posts):
        print(post)
        if id == post['id']:
            return i, post
    return None, None

@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[-1]
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="no post to show")
    return {"data": post}


@app.get("/posts/{id}")
def get_posts(id: int):
    print(type(id))
    _, post = find_post(id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return {"data": post}


@app.post("/posts")
def create_posts(post: Post):
    post_dict = post.dict()
    my_posts.append(post_dict)
    return {"data": post_dict}


@app.delete("/posts/{id}")
def delete_posts(id: int):
    index, _ = find_post(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_posts(id: int, post: Post):
    index, _ = find_post(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    post_dict = post.dict()
    my_posts[index] = post_dict
    return {"data": post_dict}