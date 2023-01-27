from datetime import datetime

from app.models.user import User
from app.schemas import UserCreate
from sqlalchemy.orm import Session


def create_user(db: Session, user: UserCreate) -> User:
    db_user = User(
        id=2,
        email=user.email,
        password=user.password,
        nickname=user.nickname,
        create_time=int(datetime.now().timestamp()),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
