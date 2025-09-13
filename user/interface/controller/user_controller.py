from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
from user.application.user_service import UserService

user_router = APIRouter(prefix="/users")

class CreateUserRequest(BaseModel):
    name: str
    email: str
    password: str

def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)

@user_router.post("", status_code=201)
def create_user(
        request: CreateUserRequest,
        user_service: UserService = Depends(get_user_service)
):
    user_service.create_user(
        name=request.name,
        email=request.email,
        password=request.password
    )

    return "ok"