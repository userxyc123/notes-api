from fastapi import APIRouter, HTTPException

from app.models.note import (
    CreateNoteRequest,
    CreateNoteResponse,
    NoteRecord,
    NoteResponse,
    UpdateNoteRequest,
)
from app.repositories.note_repository import NoteRepository

router = APIRouter(prefix="/notes", tags=["notes"])

# Single shared instance — replace with DI / lifespan state when adding DynamoDB
_repo = NoteRepository()


@router.post("", response_model=CreateNoteResponse, status_code=201)
def create_note(body: CreateNoteRequest):
    note = NoteRecord(text=body.text)
    _repo.put_item(note)
    return CreateNoteResponse(noteId=note.noteId)


@router.get("", response_model=list[NoteResponse])
def list_notes():
    return [NoteResponse(**n.model_dump()) for n in _repo.scan()]


@router.get("/{note_id}", response_model=NoteResponse)
def get_note(note_id: str):
    note = _repo.get_item(note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return NoteResponse(**note.model_dump())


@router.patch("/{note_id}", response_model=NoteResponse)
def update_note(note_id: str, body: UpdateNoteRequest):
    note = _repo.update_item(note_id, body.text)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return NoteResponse(**note.model_dump())


@router.delete("/{note_id}", status_code=204)
def delete_note(note_id: str):
    if not _repo.delete_item(note_id):
        raise HTTPException(status_code=404, detail="Note not found")
