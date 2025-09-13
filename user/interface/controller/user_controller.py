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

class UpdateUserRequest(BaseModel):
    name: str | None = None
    password: str | None = None


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

@user_router.put("/{user_id}", status_code=200)
def update_user(
        user_id: str,
        request: UpdateUserRequest,
        user_service: UserService = Depends(get_user_service)
):
    updated_user = user_service.update_user(
        user_id=user_id,
        name=request.name,
        password=request.password
    )

    return updated_user
