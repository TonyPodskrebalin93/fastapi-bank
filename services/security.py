from jose import jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException

import crud

SECRET_KEY = "super_secret_key_123456"

ALGORITHM = "HS256"


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({
        "exp": expire
    })
    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def verify_token(token: str, db):
    payload = jwt.decode(token,
                         SECRET_KEY,
                         algorithms=[ALGORITHM])

    user_id = payload.get("user_id")
    if user_id is None:
        raise HTTPException(status_code=401,
                            detail="invalid token")
    user = crud.get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=401,
                            detail="invalid token")

    return user
