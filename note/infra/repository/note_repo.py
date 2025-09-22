from sqlalchemy.orm import Session

from note.infra.model.note import Note
from note.repository.note_repo import INoteRepository
from user.domain.user import User


class NoteRepository(INoteRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_notes_by_user_id(
            self,
            user_id: str,
            page: int,
            items_per_page: int
    ) -> tuple[int, list[Note]]:
        query = (
            self.session.query(Note)
                .filter(Note.user_id == user_id)
            .offset((page - 1) * items_per_page)
            .limit(items_per_page)
        )

        total_count = query.count()
        notes = query.all()

        return total_count, notes

    def save(self, user: User):
        raise NotImplementedError

    def find_by_email(self, email: str) -> User:
        raise NotImplementedError

    def find_by_id(self, user_id: str) -> User:
        raise NotImplementedError

    def update(self, user: User):
        raise NotImplementedError

    def get_users(self, page: int, items_per_age: int) -> tuple[int, list[User]]:
        raise NotImplementedError
