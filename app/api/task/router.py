from fastapi import APIRouter, Depends, HTTPException, status
from app.services.task import TaskService
from app.schemas.task import TaskCreate, TaskInDB, TaskUpdate

router = APIRouter(
    prefix="/tasks",
    tags=["Task Management"],
    responses={
        401: {"description": "Unauthorized"},
        404: {"description": "Task not found"},
        422: {"description": "Validation error"},
    },
)


def get_task_service() -> TaskService:
    return TaskService()


@router.get(
    "",
    response_model=list[TaskInDB],
    summary="Get all tasks",
    description="Retrieve a list of all tasks",
)
async def get_tasks(
    service: TaskService = Depends(get_task_service), skip: int = 0, limit: int = 10
) -> list[TaskInDB]:
    try:
        tasks = await service.get_tasks(skip, limit)
        return [TaskInDB.model_validate(task) for task in tasks]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.post(
    "",
    response_model=TaskInDB,
    summary="Create a new task",
    description="Create a new task with the given details",
)
async def create_task(
    task: TaskCreate,
    service: TaskService = Depends(get_task_service),
) -> TaskInDB:
    try:
        new_task = await service.create_task(task)
        return TaskInDB.model_validate(new_task)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get(
    "/{task_id}",
    response_model=TaskInDB,
    summary="Get a task by ID",
    description="Retrieve a task by its unique identifier",
)
async def get_task(
    task_id: int,
    service: TaskService = Depends(get_task_service),
) -> TaskInDB:
    try:
        task = await service.get_task(task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
            )
        return TaskInDB.model_validate(task)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.put(
    "/{task_id}",
    response_model=TaskInDB,
    summary="Update a task",
    description="Update a task with the given details",
)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    service: TaskService = Depends(get_task_service),
) -> TaskInDB:
    try:
        updated_task = await service.update_task(task_id, task_update)
        return TaskInDB.model_validate(updated_task)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.delete(
    "/{task_id}",
    summary="Delete a task",
    description="Delete a task with the given ID",
)
async def delete_task(
    task_id: int,
    service: TaskService = Depends(get_task_service),
) -> None:
    try:
        await service.delete_task(task_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
