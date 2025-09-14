from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field, EmailStr
from sqlalchemy.orm import Session

from database import get_db
from user.application.user_service import UserService
from user.domain.user import User

user_router = APIRouter(prefix="/users")


class CreateUserRequest(BaseModel):
    name: str = Field(min_length=2, max_length=32)
    email: EmailStr = Field(max_length=64)
    password: str = Field(min_length=8, max_length=32)

class UpdateUserRequest(BaseModel):
    name: str = Field(default=None, min_length=2, max_length=32)
    password: str = Field(default=None, min_length=8, max_length=32)


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)

@user_router.get("", status_code=200)
def get_users(
        user_service: UserService = Depends(get_user_service),
        page: int = 1,
        items_per_page: int = 10,
):
    total_count, users = user_service.get_users(page, items_per_page)

    return {
        "total_count": total_count,
        "page": page,
        "users": users
    }

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

@user_router.delete("/{user_id}", status_code=204)
def delete_user(
        user_id: str,
        user_service: UserService = Depends(get_user_service)
):
    """
    현재 문제점: user_id만 알고 있으면 사용자를 삭제할 수 있다.
    TODO: JWT 인증/인가 도입 시 토큰에서 user_id 추출하여 사용자를 삭제할 수 있도록 한다.
    """

    user_service.delete_user(user_id=user_id)