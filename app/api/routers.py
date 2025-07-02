from fastapi import APIRouter
from app.api.task.router import router as task_router


routers = APIRouter(
    prefix="/api",
    tags=["API"],
    responses={
        404: {"description": "Not found"},
        500: {"description": "Internal server error"},
    },
)

router_list = [
    task_router,
]

for router in router_list:
    routers.include_router(router)


def get_api_router() -> APIRouter:
    return routers
