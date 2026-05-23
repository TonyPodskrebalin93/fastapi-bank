from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    age: int

class UserResponse(BaseModel):
    id: int
    name: str
    age: int

    class Config:
        from_attributes =True