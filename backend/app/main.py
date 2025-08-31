from datetime import datetime
from enum import Enum
from typing import List

from fastapi import FastAPI, Depends, HTTPException, Path, Query, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, constr
from sqlalchemy.orm import Session

import app.models as models
from app.database import SessionLocal, engine, Base

# -----------------------------
# Database setup
# -----------------------------
Base.metadata.create_all(bind=engine)

# -----------------------------
# FastAPI app
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
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
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

    model_config = {"from_attributes": True}


class TaskUpdate(BaseModel):
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
# WebSocket connections
# -----------------------------
active_connections: List[WebSocket] = []

async def broadcast(message: dict):
    for connection in active_connections.copy():
        try:
            await connection.send_json(message)
        except Exception:
            if connection in active_connections:
                active_connections.remove(connection)

@app.websocket("/ws/tasks")
async def ws_tasks(ws: WebSocket):
    await ws.accept()
    active_connections.append(ws)
    try:
        while True:
            try:
                await ws.receive_text()
            except WebSocketDisconnect:
                break
    finally:
        if ws in active_connections:
            active_connections.remove(ws)


# -----------------------------
# CRUD endpoints
# -----------------------------
@app.get("/api/tasks")
async def list_tasks(
        status: str | None = Query(None),
        skip: int = Query(0, ge=0),
        limit: int = Query(10, gt=0),
        db: Session = Depends(get_db)
):
    query = db.query(models.Task)
    if status:
        if status not in TASK_STATUSES:
            raise HTTPException(status_code=400, detail="Invalid status")
        query = query.filter(models.Task.status == status)

    # Сортировка по дате создания, новые записи сверху
    query = query.order_by(models.Task.id.desc())

    total = query.count()
    tasks = query.offset(skip).limit(limit).all()
    return {"total": total, "tasks": tasks}


@app.post("/api/tasks", response_model=TaskSchema)
async def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    db_task = models.Task(
        title=task.title,
        description=task.description,
        status=task.status
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    await broadcast({
        "event": "created",
        "task": {
            "id": db_task.id,
            "title": db_task.title,
            "description": db_task.description,
            "status": db_task.status,
            "created_at": db_task.created_at.isoformat()
        }
    })

    return db_task

@app.put("/api/tasks/{task_id}", response_model=TaskSchema)
async def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.title is not None:
        db_task.title = task.title
    if task.description is not None:
        db_task.description = task.description
    if task.status is not None:
        db_task.status = task.status

    db.commit()
    db.refresh(db_task)

    await broadcast({
        "event": "updated",
        "task": {
            "id": db_task.id,
            "title": db_task.title,
            "description": db_task.description,
            "status": db_task.status,
            "created_at": db_task.created_at.isoformat()
        }
    })

    return db_task

@app.delete("/api/tasks/{task_id}")
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(db_task)
    db.commit()

    await broadcast({
        "event": "deleted",
        "task_id": task_id
    })

    return {"detail": "Task deleted"}
