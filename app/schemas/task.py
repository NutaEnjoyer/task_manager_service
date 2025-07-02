from datetime import datetime
from typing import Optional
import enum

from pydantic import BaseModel


class TaskStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    title: Optional[str] = None
    status: Optional[TaskStatus] = None


class TaskInDB(TaskBase):
    id: int
    status: TaskStatus

    model_config = {"from_attributes": True}
