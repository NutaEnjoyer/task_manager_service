from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.routers import get_api_router
from app.core.database import create_tables


router = get_api_router()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield


app = FastAPI(
    title="Task Management API",
    description="API for managing tasks",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.include_router(router)


@app.get("/", tags=["Health Check"])
def health_check():
    return {"health": "check"}
