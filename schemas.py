from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    age: int
    email: str
    password: str


class UserUpdate(BaseModel):
    name: str | None = None

    age: int | None = None


class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    age: int


class LoginRequest(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        from_attributes = True
