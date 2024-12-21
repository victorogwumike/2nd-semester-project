from fastapi import APIRouter, HTTPException
from models import User
from typing import List

router = APIRouter()

users_db = []

@router.post("/users/", response_model=User)
def create_user(user: User):
    if any(u.email == user.email for u in users_db):
        raise HTTPException(status_code=400, detail="Email already registered")
    users_db.append(user)
    return user

@router.get("/users/", response_model=List[User])
def get_users():
    return users_db

@router.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, updated_user: User):
    for user in users_db:
        if user.id == user_id:
            user.name = updated_user.name
            user.email = updated_user.email
            return user
    raise HTTPException(status_code=404, detail="User not found")

@router.delete("/users/{user_id}", response_model=User)
def delete_user(user_id: int):
    for user in users_db:
        if user.id == user_id:
            users_db.remove(user)
            return user
    raise HTTPException(status_code=404, detail="User not found")

@router.post("/users/{user_id}/deactivate", response_model=User)
def deactivate_user(user_id: int):
    for user in users_db:
        if user.id == user_id:
            user.is_active = False
            return user
    raise HTTPException(status_code=404, detail="User not found")
