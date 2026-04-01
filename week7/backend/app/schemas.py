from datetime import datetime
from typing import List

from pydantic import BaseModel, field_validator, model_validator


class NoteCreate(BaseModel):
    title: str
    content: str


class NoteRead(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class NotePatch(BaseModel):
    title: str | None = None
    content: str | None = None


class NoteSearchRequest(BaseModel):
    query: str
    limit: int = 20
    sort: str = "-created_at"

    @field_validator("query")
    @classmethod
    def validate_query(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("query must not be empty")
        if len(v) > 200:
            raise ValueError("query must be at most 200 characters")
        return v

    @field_validator("limit")
    @classmethod
    def validate_limit(cls, v: int) -> int:
        if v < 1 or v > 100:
            raise ValueError("limit must be between 1 and 100")
        return v

    @field_validator("sort")
    @classmethod
    def validate_sort(cls, v: str) -> str:
        allowed_sorts = {"created_at", "-created_at", "title", "-title"}
        if v not in allowed_sorts:
            raise ValueError(f"sort must be one of {sorted(allowed_sorts)}")
        return v


class ActionItemCreate(BaseModel):
    description: str


class ActionItemRead(BaseModel):
    id: int
    description: str
    completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ActionItemPatch(BaseModel):
    description: str | None = None
    completed: bool | None = None


class ActionItemsBulkCreateRequest(BaseModel):
    items: List[ActionItemCreate]

    @model_validator(mode="after")
    def validate_items(self) -> "ActionItemsBulkCreateRequest":
        if not self.items:
            raise ValueError("items must contain at least one item")
        if len(self.items) > 50:
            raise ValueError("items must not contain more than 50 items")
        return self


