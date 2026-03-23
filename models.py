from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Category(Base):
    """Todo 항목을 분류하는 카테고리 테이블"""

    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    color: Mapped[Optional[str]] = mapped_column(String(7), default="#3b82f6")  # HEX 색상 코드

    # 역참조: 이 카테고리에 속한 모든 Todo 목록
    todos: Mapped[list["Todo"]] = relationship("Todo", back_populates="category")


class Todo(Base):
    """할 일 항목 테이블"""

    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    priority: Mapped[int] = mapped_column(Integer, default=2)  # 1=높음, 2=보통, 3=낮음
    due_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    # 외래키: categories.id 를 참조
    category_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("categories.id", ondelete="SET NULL"), nullable=True
    )

    # 관계: 연결된 Category 객체에 접근
    category: Mapped[Optional[Category]] = relationship("Category", back_populates="todos")
