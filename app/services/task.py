from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.core.database import new_session
from app.core.telegram_notify import notify_telegram
from app.models.task import Task, TaskStatus
from app.redis_pubsub.publisher import publish_task_event
from app.schemas.task import TaskCreate, TaskUpdate


class TaskService:
    def __init__(self, session: async_sessionmaker[AsyncSession] = new_session):
        self.session = session

    async def create_task(self, tesk: TaskCreate) -> Task:
        async with self.session() as session:
            task_dict = tesk.model_dump()
            db_task = Task(**task_dict)
            session.add(db_task)
            await session.commit()
            await session.refresh(db_task)

            await publish_task_event(
                {"action": "create", "task_id": db_task.id, "task_title": db_task.title}
            )

            return db_task

    async def update_task(self, task_id: int, task_update: TaskUpdate) -> Task:
        async with self.session() as session:
            db_task = await session.get(Task, task_id)
            if not db_task:
                raise HTTPException(status_code=404, detail="Task not found")

            old_status = db_task.status
            task_dict = task_update.model_dump(exclude_unset=True)
            for field, value in task_dict.items():
                setattr(db_task, field, value)

            await session.flush()
            await session.commit()
            await session.refresh(db_task)

            if old_status != TaskStatus.DONE and db_task.status == TaskStatus.DONE:
                await notify_telegram(
                    f"Task#{task_id} {db_task.title} has been completed!"
                )

            return db_task

    async def get_task(self, task_id: int) -> Task | None:
        async with self.session() as session:
            db_task = await session.get(Task, task_id)
            if not db_task:
                return None
            return db_task

    async def get_tasks(self, skip: int = 0, limit: int = 10) -> list[Task]:
        async with self.session() as session:
            query = select(Task).offset(skip).limit(limit)
            result = await session.execute(query)
            tasks = list(result.scalars().all())
            return tasks

    async def delete_task(self, task_id: int) -> None:
        async with self.session() as session:
            db_task = await session.get(Task, task_id)
            if not db_task:
                raise HTTPException(status_code=404, detail="Task not found")
            await session.delete(db_task)
            await session.commit()
            return None
