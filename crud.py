from models import UserDB
from sqlalchemy.orm import Session


def get_all_users(db: Session):
    return db.query(UserDB).all()


def get_user_by_id(db: Session, user_id: int):
    return db.query(UserDB).filter(UserDB.id == user_id).first()


# def hello_user(db: Session, name: str):
#     return db.query(UserDB).filter(UserDB.name == name).first()


def get_by_name(db: Session, name: str):
    return db.query(UserDB).filter(UserDB.name == name).first()


def user_delete(db: Session, user_id: int):
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return user


def update_user(db: Session, user_id: int, user_data):
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if user is None:
        return None
    update_data = user_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user
