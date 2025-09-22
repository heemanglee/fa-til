from sqlalchemy.orm import Session

from note.infra.repository.note_repo import NoteRepository
from note.repository.note_repo import INoteRepository


class NoteService:
    def __init__(self, session: Session):
        self.note_repo: INoteRepository = NoteRepository(session)

    def get_notes_by_user_id(
            self,
            user_id: str,
            page: int,
            items_per_page: int,
    ):
        total_count, notes = self.note_repo.get_notes_by_user_id(
            user_id=user_id,
            page=page,
            items_per_page=items_per_page
        )

        return total_count, notes
