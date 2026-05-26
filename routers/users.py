from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
# from pydantic import BaseModel
from database import get_db
from models import UserDB
from schemas import UserResponse, UserCreate, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])







@router.get("/", response_model=list[UserResponse])
def get_user(db: Session = Depends(get_db)):
    all_user = db.query(UserDB).all()
    return all_user


@router.get("/id/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404,
                            detail="User not found!")
    return user


@router.get("/hello/{name}")
def hello_users(name: str, db: Session = Depends(get_db)):
    greeting_user = db.query(UserDB).filter(UserDB.name == name).first()
    if greeting_user is None:
        raise HTTPException(status_code=404,
                            detail="User not found!")
    return {"message": f"Hello {name}!"}


@router.get("/sum/{a}/{b}")
def get_sum(a: int, b: int):
    return {
        "result":
            a + b
    }


@router.post("/name")
def create_message(user: UserCreate):
    return {"message": f"Hello {user.name}!"}


@router.post("/users_db", response_model=UserResponse,
             status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = UserDB(name=user.name,
                     age=user.age)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# @app.post("/users", status_code=status.HTTP_201_CREATED)
# def add_user(user: User):
#     db = SessionLocal()
#
#     existing_user = db.query(UserDB).filter(UserDB.name == user.name).first()
#
#     if existing_user:
#         raise HTTPException(status_code=400,
#                             detail="User already exists!")
#
#     new_user = UserDB(name=user.name,
#                       age=user.age)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#
#     return new_user


@router.get("/{name}", response_model=UserResponse)
def get_user_by_name(name: str, db: Session = Depends(get_db)):
    user_get = db.query(UserDB).filter(UserDB.name == name).first()
    if user_get is None:
        raise HTTPException(status_code=404,
                            detail="User not found!")

    return user_get


@router.delete("/{name}")
def delete_user(name: str, db: Session = Depends(get_db)):
    user_del = db.query(UserDB).filter(UserDB.name == name).first()
    if user_del is None:
        raise HTTPException(status_code=404, detail="User not found!")
    else:
        db.delete(user_del)
        db.commit()
        return {"status": "success",
                "message": f"User {name} is deleted!"}


@router.put("/{name}", response_model=UserResponse)
def update_user(name: str, user: UserUpdate, db: Session = Depends(get_db)):
    user_up = db.query(UserDB).filter(UserDB.name == name).first()
    if user_up is None:
        raise HTTPException(status_code=404,
                            detail="User not found!")
    update_user = user.model_dump(exclude_unset=True)

    for key, value in update_user.items():
        setattr(user_up, key, value)

    db.commit()
    db.refresh(user_up)
    return user_up
