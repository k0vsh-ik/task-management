from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from app import models, schemas, websockets, constants
from app.database import get_db

router = APIRouter(prefix="/api/tasks", tags=["Tasks"])

async def broadcast_task(event: str, task: models.Task):
    await websockets.broadcast({
        "event": event,
        "task": {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "created_at": task.created_at.isoformat()
        }
    })

@router.get("")
async def list_tasks(
    status: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, gt=0),
    db: Session = Depends(get_db)
):
    query = db.query(models.Task)
    if status:
        if status not in constants.TASK_STATUSES:
            raise HTTPException(status_code=400, detail="Invalid status")
        query = query.filter(models.Task.status == status)

    total = query.count()
    tasks = query.order_by(models.Task.id.desc()).offset(skip).limit(limit).all()
    return {"total": total, "tasks": tasks}

@router.post("", response_model=schemas.TaskSchema)
async def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    db_task = models.Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    await broadcast_task("created", db_task)
    return db_task

@router.put("/{task_id}", response_model=schemas.TaskSchema)
async def update_task(task_id: int, task: schemas.TaskUpdate, db: Session = Depends(get_db)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    for field, value in task.model_dump(exclude_unset=True).items():
        setattr(db_task, field, value)

    db.commit()
    db.refresh(db_task)

    await broadcast_task("updated", db_task)
    return db_task

@router.delete("/{task_id}")
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(db_task)
    db.commit()

    await websockets.broadcast({"event": "deleted", "task_id": task_id})
    return {"detail": "Task deleted"}
