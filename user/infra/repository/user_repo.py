from fastapi import HTTPException
from sqlalchemy.orm import Session

from user.domain.user import User as UserVO
from user.infra.model.user import User
from user.repository.user_repo import IUserRepository


class UserRepository(IUserRepository):
    def __init__(self, db: Session):
        self.db = db

    def save(self, user: UserVO):
        new_user = User(
            id=user.id,
            name=user.name,
            email=user.email,
            password=user.password,
            memo=user.memo,
            created_at=user.created_at,
            updated_at=user.updated_at
        )

        self.db.add(new_user)
        self.db.commit()

    def find_by_email(self, email: str) -> UserVO:
        find_user = self.db.query(User).filter(User.email == email).first()

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

    def find_by_id(self, user_id: str) -> UserVO:
        find_user = self.db.query(User).filter(User.id == user_id).first()

        if not find_user:
            raise HTTPException(status_code=404, detail=f"User Not Found, userId={user_id}")

        return UserVO(
            id=find_user.id,
            name=find_user.name,
            email=find_user.email,
            password=find_user.password,
            created_at=find_user.created_at,
            updated_at=find_user.updated_at
        )

    def update(self, user_vo: UserVO):
        user = self.db.query(User).filter(User.id == user_vo.id).first()

        if not user:
            raise HTTPException(status_code=404, detail=f"User Not Found, userId={user.id}")

        user.name = user_vo.name,
        user.password = user_vo.password

        self.db.commit()
        self.db.close()

        return user
