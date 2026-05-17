from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel


class User(BaseModel):
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


@app.post("/users")
def add_user(user: User):
    users.append(user)
    return {"status": "success",
            "user_count": len(users)
            }


@app.delete("/user/{name}")
def delete_user(name: str):
    for user in users:
        if user.name == name:
            users.remove(user)
            return {"status": "success",
                    "message": f"User {name} is deleted!"}

    return {"status": "error",
            "message": "User not found!"}


@app.put("/user/{name}")
def update_user(name: str, age: int):
    for user in users:
        if user.name == name:
            user.age = age
            return {"status": "success",
                    "message": f"User {name} is updated!"}
    return {"status": "error",
            "message": "User not found!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8010)
