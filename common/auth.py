from datetime import datetime, timedelta

from fastapi import HTTPException, status
from jose import JWTError, jwt

SECRET_KEY = "TEST_SECRET_KEY"
ALGORITHM = "HS256"

def create_access_token(
        payload: dict,
        expires_delta: timedelta = timedelta(hours=1)
):
    now = datetime.utcnow()
    expired = now + expires_delta

    payload.update({"exp": expired})
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def decode_access_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)