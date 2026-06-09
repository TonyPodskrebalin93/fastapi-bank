from fastapi import HTTPException

import crud
from sqlalchemy.orm import Session

from schemas import UserCreate


def create_user_service(db: Session, user: UserCreate):
    if user.age < 18 or user.age > 120:
        raise HTTPException(status_code=400,
                            detail="User must be at least 18 years old and higher than 120 years old")
    elif len(user.name) < 3:
        raise HTTPException(status_code=400,
                            detail="User must be at least 3 characters long")
    existing_user = crud.get_by_name(db, name=user.name)
    if existing_user:
        raise HTTPException(status_code=400,
                            detail="User already exists")

    return crud.create_user(db, user)
