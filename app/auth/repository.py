from sqlalchemy.orm import Session
from .models import User
from typing import List, Optional


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()

    def create_user(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update_user(self, email: str, user_info: dict) -> int:
        result = self.db.query(User).filter(User.email == email).update(user_info)
        self.db.commit()
        return result

    def get_all_users(self, email: str) -> List[User]:
        return self.db.query(User).filter(User.email != email).all()
