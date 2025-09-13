from fastapi import APIRouter
from pydantic import BaseModel

user_router = APIRouter(prefix="/users")

class CreateUserRequest(BaseModel):
    name: str
    email: str
    password: str

@user_router.post("", status_code=201)
def create_user(request: CreateUserRequest):
    return request