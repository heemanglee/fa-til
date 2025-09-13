from fastapi import HTTPException

from database import SessionLocal
from user.domain.user import User as UserVO
from user.infra.model.user import User
from user.repository.user_repo import IUserRepository


class UserRepository(IUserRepository):
    def save(self, user: UserVO):
        new_user = User(
            id=user.id,
            name=user.name,
            email=user.email,
            password=user.password,
            created_at=user.created_at,
            updated_at=user.updated_at
        )

        with SessionLocal() as db:
            try:
                db = SessionLocal()
                db.add(new_user)
                db.commit()
            finally:
                db.close()

    def find_by_email(self, email: str) -> User :
        with SessionLocal() as db:
            find_user = db.query(User).filter(User.email == email).first()

        if find_user:
            return UserVO(
                id=find_user.id,
                name=find_user.name,
                email=find_user.email,
                password=find_user.password,
                created_at=find_user.created_at,
                updated_at=find_user.updated_at
            )

        raise HTTPException(status_code=422)