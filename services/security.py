from jose import jwt, JWTError

from datetime import datetime, timedelta
from fastapi import HTTPException
from passlib.context import CryptContext

import crud

SECRET_KEY = "super_secret_key_123456"

ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"],
                           deprecated="auto")


def hash_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


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
    try:
        payload = jwt.decode(token,
                             SECRET_KEY,
                             algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401,
                            detail="invalid token")

    user_id = payload.get("user_id")
    if user_id is None:
        raise HTTPException(status_code=401,
                            detail="invalid token")
    user = crud.get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=401,
                            detail="invalid token")

    return user
