from datetime import datetime
from enum import Enum
from pydantic import BaseModel, constr

NonEmptyStr = constr(min_length=1)

class TaskStatus(str, Enum):
    pending = "To Do"
    in_progress = "In Progress"
    done = "Done"

class TaskCreate(BaseModel):
    title: NonEmptyStr
    description: NonEmptyStr
    status: TaskStatus

class TaskUpdate(BaseModel):
    title: NonEmptyStr | None = None
    description: NonEmptyStr | None = None
    status: TaskStatus | None = None

class TaskSchema(BaseModel):
    id: int
    title: str
    description: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
