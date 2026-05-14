from fastapi import Depends
from sqlalchemy.orm import Session
from config import get_settings
from src.db.database import get_db
from src.models.user import UserService
from src.db.users_repository import UserRepository

def get_user_storage(db: Session = Depends(get_db)):
    settings = get_settings()
    if settings.TEST_MODE:
        return UserService() 
    return UserRepository(db)