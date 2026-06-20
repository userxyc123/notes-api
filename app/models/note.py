import uuid
from datetime import datetime, timezone
from pydantic import BaseModel, Field


# NoSQL Data Model — designed for AWS DynamoDB
#
# Table name : Notes
# Partition key : noteId  (String, UUID)
# No sort key required for single-item access patterns
#
# GSI candidate (future):
#   Index name  : createdAt-index
#   Partition key: a static shard key (e.g. "ALL") so notes can be listed in
#                  time order without a full table Scan.

class NoteRecord(BaseModel):
    """DynamoDB item schema for the Notes table."""
    noteId: str = Field(default_factory=lambda: str(uuid.uuid4()))
    text: str
    createdAt: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    updatedAt: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )


# --- Request / Response shapes ---

class CreateNoteRequest(BaseModel):
    text: str


class UpdateNoteRequest(BaseModel):
    text: str


class CreateNoteResponse(BaseModel):
    noteId: str


class NoteResponse(BaseModel):
    noteId: str
    text: str
    createdAt: str
    updatedAt: str
