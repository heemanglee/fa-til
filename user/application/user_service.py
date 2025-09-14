from datetime import datetime

import ulid
from fastapi import HTTPException
from sqlalchemy.orm import Session

from user.domain.user import User
from user.infra.repository.user_repo import UserRepository
from user.repository.user_repo import IUserRepository
from utils.crypto import Crypto


class UserService:
    def __init__(self, db: Session):
        self.user_repo: IUserRepository = UserRepository(db)
        self.crypto = Crypto()

    def get_users(self) -> list[User]:
        return self.user_repo.get_users()

    def create_user(self, name: str, email: str, password: str, memo: str = None):
        _user = None

        # 가입되어 있는 이메일일 경우 예외가 발생합니다.
        try:
            _user = self.user_repo.find_by_email(email)
        except HTTPException as e:
            if e.status_code != 422:
                raise e

        if _user:
            raise HTTPException(status_code=422, detail=f"User already exists, email={email}")

        now = datetime.now()
        user: User = User(
            id=str(ulid.new()),
            name=name,
            email=email,
            password=self.crypto.pwd_context.encrypt(password),
            memo=memo,
            created_at=now,
            updated_at=now
        )

        self.user_repo.save(user)
        return user

    def update_user(
            self,
            user_id: str,
            name: str | None = None,
            password: str | None = None,
    ):
        find_user = self.user_repo.find_by_id(user_id)

        if name:
            find_user.name = name
        if password:
            find_user.password = self.crypto.encrypt(password)
        find_user.updated_at = datetime.now()

        self.user_repo.update(find_user)

        return find_user
