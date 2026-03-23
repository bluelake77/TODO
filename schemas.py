from datetime import datetime
import re
from typing import Optional

from pydantic import BaseModel, Field, field_validator


# ─────────────────────────── Category ───────────────────────────

class CategoryCreate(BaseModel):
    name: str = Field(..., max_length=100)
    color: Optional[str] = "#3b82f6"

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Category name cannot be empty")
        return v

    @field_validator("color")
    @classmethod
    def validate_color(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        v = v.strip()
        if not re.fullmatch(r"#[0-9A-Fa-f]{6}", v):
            raise ValueError("color must be a HEX code like #1A2B3C")
        return v


class CategoryResponse(BaseModel):
    id: int
    name: str
    color: Optional[str]

    model_config = {"from_attributes": True}


# ─────────────────────────── Todo ───────────────────────────────

class TodoCreate(BaseModel):
    title: str = Field(..., max_length=200)
    description: Optional[str] = None
    priority: int = Field(default=2, ge=1, le=3)  # 1=높음, 2=보통, 3=낮음
    due_date: Optional[datetime] = None
    category_id: Optional[int] = None

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Title cannot be empty")
        return v


class TodoUpdate(BaseModel):
    title: Optional[str] = Field(default=None, max_length=200)
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[int] = Field(default=None, ge=1, le=3)
    due_date: Optional[datetime] = None
    category_id: Optional[int] = None

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            v = v.strip()
            if not v:
                raise ValueError("Title cannot be empty")
        return v


class TodoResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    completed: bool
    priority: int
    due_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    category_id: Optional[int]
    category: Optional[CategoryResponse]

    model_config = {"from_attributes": True}
