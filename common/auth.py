from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import StrEnum

from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

SECRET_KEY = "TEST_SECRET_KEY"
ALGORITHM = "HS256"


class Role(StrEnum):
    ADMIN = "ADMIN",
    USER = "USER",


oauth2_schema = OAuth2PasswordBearer(tokenUrl="/users/login")


@dataclass
class CurrentUser:
    user_id: str
    role: Role


def get_current_user(token: str = Depends(oauth2_schema)):
    try:
        payload = decode_access_token(token)
        user_id = payload.get("user_id")
        role = payload.get("role")

        if not user_id or not role:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

        return CurrentUser(user_id=user_id, role=role)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


def create_access_token(
        payload: dict,
        expires_delta: timedelta = timedelta(hours=1)
):
    now = datetime.utcnow()
    expired = now + expires_delta

    payload.update({
        "exp": expired,
    })
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def decode_access_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
