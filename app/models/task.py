from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Enum as SQLEnum
from sqlalchemy.orm import mapped_column, Mapped

from app.models.base import Base
from app.schemas.task import TaskStatus


class Task(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, index=True, nullable=False)
    description: Mapped[str] = mapped_column(String)
    due_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[TaskStatus] = mapped_column(
        SQLEnum(TaskStatus), default=TaskStatus.PENDING
    )
