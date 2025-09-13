from fastapi import APIRouter
from pydantic import BaseModel

from user.application.user_service import UserService

user_router = APIRouter(prefix="/users")

class CreateUserRequest(BaseModel):
    name: str
    email: str
    password: str

@user_router.post("", status_code=201)
def create_user(request: CreateUserRequest):
    user_service = UserService()
    user_service.create_user(
        name=request.name,
        email=request.email,
        password=request.password
    )

    return "ok"