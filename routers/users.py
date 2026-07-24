from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session


import crud
from database import get_db
from models import UserDB
from services.auth_service import get_current_user, require_admin
from fastapi.security import OAuth2PasswordRequestForm

from schemas import UserResponse, UserCreate, UserUpdate, Token
from services.user_service import create_user_service
from services.auth_service import login

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/profile", response_model=UserResponse)
def profile(current_user: UserDB = Depends(get_current_user)):
    return current_user


@router.get("/admin/users", response_model=list[UserResponse])
def admin_user(db: Session = Depends(get_db),
            current_user: UserDB = Depends(require_admin)):
    return crud.get_all_users(db)


@router.get("/", response_model=list[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    users = crud.get_all_users(db)
    return users


@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=404,
                            detail="User not found!")
    return user


# @router.get("/hello/{name}")
# def hello_users(name: str, db: Session = Depends(get_db)):
#     greeting_user = crud.hello_user(db, name)
#     if greeting_user is None:
#         raise HTTPException(status_code=404,
#                             detail="User not found!")
#     return {"message": f"Hello {name}!"}


# @router.get("/sum/{a}/{b}")
# def get_sum(a: int, b: int):
#     return {
#         "result":
#             a + b
#     }


@router.post("/login", response_model=Token)
def login_user(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db),
               ):
    return login(form_data, db)


@router.post("/", response_model=UserResponse,
             status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user_service(db, user)


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


@router.get("/by-name/{name}", response_model=UserResponse)
def get_user_by_name(name: str, db: Session = Depends(get_db)):
    user_get = crud.get_by_name(db, name)
    if user_get is None:
        raise HTTPException(status_code=404,
                            detail="User not found!")

    return user_get


@router.get("/by-age/{age}", response_model=list[UserResponse])
def get_user_by_age(age: int, db: Session = Depends(get_db)):
    return crud.get_users_by_age(db, age)


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: UserDB = Depends(require_admin)):
    user_del = crud.user_delete(db, user_id)
    if user_del is None:
        raise HTTPException(status_code=404, detail="User not found!")
    else:

        return {"status": "success",
                "message": f"User with {user_id} is deleted!"}


@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    user_up = crud.update_user(db, user_id, user)
    if user_up is None:
        raise HTTPException(status_code=404,
                            detail="User not found!")

    return user_up


@router.get("/older-than/{age}", response_model=list[UserResponse])
def get_users_older_than(age: int, db: Session = Depends(get_db)):
    return crud.get_users_older_than(db, age)
