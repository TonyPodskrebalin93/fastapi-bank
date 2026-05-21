from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
from fastapi import HTTPException
from fastapi import status


class User(BaseModel):
    name: str
    age: int


class UserResponse(BaseModel):
    name: str
    age: int


app = FastAPI()

users = []


@app.get("/users")
def get_user():
    return users


@app.get("/")
def say_hello():
    return {"message": "Hello Python Developer"}


@app.get("/hello/{name}")
def hello_users(name: str):
    return {"message": f"Hello {name}!"}


@app.get("/sum/{a}/{b}")
def get_sum(a: int, b: int):
    return {
        "result":
            a + b
    }


@app.post("/name")
def create_message(user: User):
    return {"message": f"Hello {user.name}!"}


@app.post("/users", status_code=status.HTTP_201_CREATED)
def add_user(user: User):
    for existing_user in users:
        if existing_user.name == user.name:
            raise HTTPException(status_code=400,
                                detail="User already exists!")
    users.append(user)
    return user


@app.get("/users/{name}", response_model=UserResponse)
def get_user_by_name(name: str):
    for user in users:
        if user.name == name:
            return user
    raise HTTPException(status_code=404,
                        detail="User not found!")


@app.delete("/user/{name}")
def delete_user(name: str):
    for user in users:
        if user.name == name:
            users.remove(user)
            return {"status": "success",
                    "message": f"User {name} is deleted!"}

    return {"status": "error",
            "message": "User not found!"}


@app.put("/user/{name}", response_model=UserResponse)
def update_user(name: str, updated_user: User):
    for user in users:
        if user.name == name:
            user.name = updated_user.name
            user.age = updated_user.age
            return user

    raise HTTPException(status_code=404,
                        detail="User not found!")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8010)
