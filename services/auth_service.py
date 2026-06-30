from fastapi import HTTPException
from sqlalchemy.orm import Session

import crud
from schemas import LoginRequest
from services.security import verify_password, create_access_token


def login(user_data:LoginRequest, db:Session):
    user = crud.get_user_by_email(db, email=user_data.email)
    if user is None:
        raise HTTPException(status_code=401,
                            detail="Invalid credentials")
    if not verify_password(user_data.password, user.password):
        raise HTTPException(status_code=401,
                            detail="Invalid credentials")
    token = create_access_token({"user_id":
                                     user.id})
    return {"access_token": token,
            "token_type": "bearer"}
