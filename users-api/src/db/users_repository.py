from typing import List, Optional
import uuid
from sqlalchemy.orm import Session
from src.db.entities import User as UserEntity
from src.models.user import User as UserModel

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user_model: UserModel) -> UserModel:
        db_user = UserEntity(
            id=uuid.uuid4(),
            first_name=user_model.first_name,
            last_name=user_model.last_name,
            birthday=user_model.birthday
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return user_model

    def get_users(self) -> List[UserModel]:
        users = self.db.query(UserEntity).all()
        return [UserModel(id=u.id, first_name=u.first_name, last_name=u.last_name, birthday=u.birthday) for u in users]