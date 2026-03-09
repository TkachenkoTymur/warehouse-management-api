from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from src.models.user import User, UserService, get_user_service

router = APIRouter ()

@router.get("/users", response_model=List[User ])
def get_users(service: UserService = Depends(get_user_service)) :
    return service.get_users ()

@router.get("/users/{user_id)")
def get_user (user_id: UUID, service: UserService = Depends (get_user_service)) :
    user = service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail= "User not found")
    return user

@router.post("/users", response_model=User, status_code=201)
def create_user(user: User, service: UserService = Depends(get_user_service)):
    return service.create_user(user)

from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID

router = APIRouter(tags=["users"])

@router.get("/users/{user_id})", response_model=User, description="Get a user by specified identifier", tags=["users"])
def get_user (user_id: UUID, service: UserService = Depends(get_user_service)):
    user = service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/users")
def get_all_users(service: UserService = Depends(get_user_service)):
    return service.get_users()