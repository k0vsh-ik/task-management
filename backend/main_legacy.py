from datetime import datetime
from enum import Enum

from fastapi import FastAPI, Depends, HTTPException, Path, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel, constr

from database import SessionLocal, engine, Base
import models

# -----------------------------
# Database setup: create tables
# -----------------------------
Base.metadata.create_all(bind=engine)

# -----------------------------
# FastAPI app initialization
# -----------------------------
app = FastAPI(title="Task Management API")

# -----------------------------
# Supported task statuses
# -----------------------------
TASK_STATUSES = ["To Do", "In Progress", "Done"]

class TaskStatus(str, Enum):
    pending = "To Do"
    in_progress = "In Progress"
    done = "Done"

# -----------------------------
# CORS configuration
# -----------------------------
origins = [
    "*"
    # "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # allow GET, POST, PUT, DELETE
    allow_headers=["*"],
)

# -----------------------------
# Pydantic models
# -----------------------------
class TaskCreate(BaseModel):
    title: constr(min_length=1)
    description: constr(min_length=1)
    status: TaskStatus

class TaskSchema(BaseModel):
    id: int
    title: str
    description: str
    status: str
    created_at: datetime

    class Config:
        orm_mode = True

class TaskUpdate(BaseModel):
    """Model for updating a task: all fields optional"""
    title: constr(min_length=1) | None = None
    description: constr(min_length=1) | None = None
    status: TaskStatus | None = None

# -----------------------------
# Database dependency
# -----------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -----------------------------
# API endpoints
# -----------------------------

@app.get("/api/tasks")
def list_tasks(
    status: str | None = Query(None, description="Filter tasks by status"),
    skip: int = Query(0, ge=0, description="Number of tasks to skip"),
    limit: int = Query(10, gt=0, description="Maximum number of tasks to return"),
    db: Session = Depends(get_db)
):
    """Get list of tasks with optional status filter and pagination"""
    query = db.query(models.Task)

    # Filter tasks by status if provided
    if status:
        if status not in TASK_STATUSES:
            raise HTTPException(status_code=400, detail="Invalid status")
        query = query.filter(models.Task.status == status)

    # Count total tasks after filtering
    total = query.count()

    # Apply pagination
    tasks = query.offset(skip).limit(limit).all()

    # Return tasks and total count
    return {"total": total, "tasks": tasks}


@app.post("/api/tasks", response_model=TaskSchema)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    """Create a new task"""
    if task.status not in TASK_STATUSES:
        raise HTTPException(status_code=400, detail="Invalid status")

    db_task = models.Task(
        title=task.title,
        description=task.description,
        status=task.status
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@app.put("/api/tasks/{task_id}", response_model=TaskSchema)
def update_task(
    task_id: int = Path(..., description="ID of the task to update"),
    task: TaskUpdate = None,
    db: Session = Depends(get_db)
):
    """Update an existing task"""
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.status and task.status not in TASK_STATUSES:
        raise HTTPException(status_code=400, detail="Invalid status")

    # Update fields if provided
    if task.title is not None:
        db_task.title = task.title
    if task.description is not None:
        db_task.description = task.description
    if task.status is not None:
        db_task.status = task.status

    db.commit()
    db.refresh(db_task)
    return db_task


@app.delete("/api/tasks/{task_id}")
def delete_task(
    task_id: int = Path(..., description="ID of the task to delete"),
    db: Session = Depends(get_db)
):
    """Delete a task by ID"""
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(db_task)
    db.commit()
    return {"detail": "Task deleted"}
