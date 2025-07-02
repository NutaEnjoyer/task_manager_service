import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, patch

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.services.task import TaskService
from app.models.task import TaskStatus, Base
from app.schemas.task import TaskCreate, TaskUpdate


DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture(scope="module")
async def engine():
    engine = create_async_engine(DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
async def session_factory(engine):
    return async_sessionmaker(engine, expire_on_commit=False)


@pytest_asyncio.fixture
async def service(session_factory):
    yield TaskService(session=session_factory)


@pytest.fixture(autouse=True)
def mock_redis_publish():
    with patch("app.redis_pubsub.publisher.publish_task_event", new_callable=AsyncMock):
        yield


@pytest.mark.asyncio
async def test_create_and_get_task(service):
    task_data = TaskCreate(title="Test", description="Desc", due_date=None)
    task = await service.create_task(task_data)
    assert task.id is not None
    assert task.title == "Test"

    fetched = await service.get_task(task.id)
    assert fetched.title == "Test"
