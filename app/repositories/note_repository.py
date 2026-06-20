from datetime import datetime, timezone
from typing import Optional

from app.models.note import NoteRecord


class NoteRepository:
    """
    In-memory implementation of the Notes repository.

    Method names mirror DynamoDB's API so swapping in a real DynamoDB
    implementation later requires only replacing this class:
      put_item   → dynamodb.Table.put_item
      get_item   → dynamodb.Table.get_item
      scan       → dynamodb.Table.scan (or a GSI Query for production)
      delete_item→ dynamodb.Table.delete_item
    """

    def __init__(self) -> None:
        self._store: dict[str, NoteRecord] = {}

    def put_item(self, note: NoteRecord) -> NoteRecord:
        self._store[note.noteId] = note
        return note

    def get_item(self, note_id: str) -> Optional[NoteRecord]:
        return self._store.get(note_id)

    def scan(self) -> list[NoteRecord]:
        return sorted(self._store.values(), key=lambda n: n.createdAt)

    def delete_item(self, note_id: str) -> bool:
        if note_id not in self._store:
            return False
        del self._store[note_id]
        return True

    def update_item(self, note_id: str, text: str) -> Optional[NoteRecord]:
        note = self._store.get(note_id)
        if note is None:
            return None
        note.text = text
        note.updatedAt = datetime.now(timezone.utc).isoformat()
        return note
