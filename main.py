import os
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import models
import schemas
from database import Base, engine, get_db

# Oracle 19c 운영 환경에서는 sql/oracle19c 스크립트로 스키마를 관리
# 필요할 때만 AUTO_CREATE_TABLES=true 로 자동 생성 활성화
if os.getenv("AUTO_CREATE_TABLES", "false").lower() in {"1", "true", "yes", "on"}:
    Base.metadata.create_all(bind=engine)

app = FastAPI(title="TODO App")


# ────────────────────────── Category API ──────────────────────────

@app.get("/api/categories", response_model=list[schemas.CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    return db.query(models.Category).order_by(models.Category.name).all()


@app.post("/api/categories", response_model=schemas.CategoryResponse, status_code=201)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Category).filter(models.Category.name == category.name).first()
    if existing:
        raise HTTPException(status_code=409, detail="Category name already exists")
    db_category = models.Category(**category.model_dump())
    db.add(db_category)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Category name already exists")
    db.refresh(db_category)
    return db_category


@app.delete("/api/categories/{category_id}", status_code=204)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    db_category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(db_category)
    db.commit()


# ────────────────────────── Todo API ──────────────────────────────

@app.get("/api/todos", response_model=list[schemas.TodoResponse])
def get_todos(
    completed: Optional[bool] = None,
    priority: Optional[int] = None,
    category_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    query = db.query(models.Todo)
    if completed is not None:
        query = query.filter(models.Todo.completed == completed)
    if priority is not None:
        query = query.filter(models.Todo.priority == priority)
    if category_id is not None:
        query = query.filter(models.Todo.category_id == category_id)
    return query.order_by(models.Todo.created_at.desc()).all()


@app.post("/api/todos", response_model=schemas.TodoResponse, status_code=201)
def create_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    if todo.category_id is not None:
        category = db.query(models.Category).filter(models.Category.id == todo.category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
    db_todo = models.Todo(**todo.model_dump())
    db.add(db_todo)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Invalid todo data for current schema")
    db.refresh(db_todo)
    return db_todo


@app.put("/api/todos/{todo_id}", response_model=schemas.TodoResponse)
def update_todo(todo_id: int, todo: schemas.TodoUpdate, db: Session = Depends(get_db)):
    db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    if todo.category_id is not None:
        category = db.query(models.Category).filter(models.Category.id == todo.category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
    update_data = todo.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_todo, field, value)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Invalid update data for current schema")
    db.refresh(db_todo)
    return db_todo


@app.delete("/api/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(db_todo)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Delete failed due to related data constraints")


# Static files must be mounted last so API routes take precedence
app.mount("/", StaticFiles(directory="static", html=True), name="static")
