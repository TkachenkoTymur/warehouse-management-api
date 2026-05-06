from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from src.models.user import User, UserService, get_user_service
from src.api.models.requests import CreateUserModel

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", 
            response_model=List[User], 
            summary="Get all users", 
            description="Returns a full list of warehouse users")
def get_users(service: UserService = Depends(get_user_service)):
    return service.get_users()

@router.get("/{user_id}", 
            response_model=User, 
            summary="Get user by ID", 
            description="Get a user by specified identifier")
def get_user(user_id: UUID, service: UserService = Depends(get_user_service)):
    user = service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
    return user

@router.post("/", 
             response_model=User, 
             status_code=status.HTTP_201_CREATED, 
             summary="Create new user",
             description="Adds a new user to the system with validation")
def create_user(user: CreateUserModel, service: UserService = Depends(get_user_service)):
    new_user = User(**user.model_dump())
    return service.create_user(new_user)

@router.put("/{user_id}", response_model=User, summary="Update user")
def update_user(user_id: UUID, user: User, service: UserService = Depends(get_user_service)):
    updated_user = service.update_user(user_id, user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete user")
def delete_user(user_id: UUID, service: UserService = Depends(get_user_service)):
    if not service.delete_user(user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return None