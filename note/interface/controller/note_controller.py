from datetime import datetime

from fastapi import Depends, APIRouter, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from common.auth import CurrentUser, get_current_user
from database import get_db
from note.application.note_service import NoteService

note_router = APIRouter(prefix="/notes")


class TagResponse(BaseModel):
    id: str
    name: str


class GetNotesResponse(BaseModel):
    id: str
    user_id: str
    title: str
    content: str
    memo_date: datetime
    tags: list[TagResponse]
    created_at: datetime
    updated_at: datetime


class GetNotesListResponse(BaseModel):
    total_count: int
    notes: list[GetNotesResponse]


def get_note_service(session: Session = Depends(get_db)) -> NoteService:
    return NoteService(session)


@note_router.get("", response_model=GetNotesListResponse)
def get_notes_by_user_id(
        page: int = Query(default=1),
        items_per_page: int = Query(default=10),
        current_user: CurrentUser = Depends(get_current_user),
        note_service: NoteService = Depends(get_note_service),
) -> GetNotesListResponse:
    total_count, notes = note_service.get_notes_by_user_id(
        user_id=current_user.user_id,
        page=page,
        items_per_page=items_per_page,
    )

    response = []

    for note in notes:
        response.append(
            GetNotesResponse(
                id=note.id,
                user_id=note.user_id,
                title=note.title,
                content=note.content,
                memo_date=note.memo_date,
                tags=[TagResponse(
                    id=tag.id,
                    name=tag.name
                ) for tag in note.tags],
                created_at=note.created_at,
                updated_at=note.updated_at,
            )
        )

    return GetNotesListResponse(
        total_count=total_count,
        notes=response
    )
