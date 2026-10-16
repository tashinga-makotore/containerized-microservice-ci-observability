import logging
from time import perf_counter

from fastapi import FastAPI, HTTPException, Path, Request

from app.models import TaskCreate
from app.service import create_task, get_task, get_tasks


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger("ops-microservice")


app = FastAPI(
    title="OPS Microservice",
    description="A lightweight service for monitoring and managing processing tasks.",
    version="1.0.0",
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = perf_counter()

    try:
        response = await call_next(request)

        duration_ms = (
            perf_counter() - start_time
        ) * 1000

        logger.info(
            "%s %s -> %s (%.2f ms)",
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
        )

        return response

    except Exception:
        duration_ms = (
            perf_counter() - start_time
        ) * 1000

        logger.exception(
            "%s %s -> ERROR (%.2f ms)",
            request.method,
            request.url.path,
            duration_ms,
        )

        raise


@app.get("/")
def read_root():
    return {
        "service": "OPS Microservice",
        "status": "online",
        "version": "1.0.0",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
    }


@app.get("/status")
def service_status():
    return {
        "service": "OPS Microservice",
        "status": "operational",
        "environment": "local",
    }


@app.get("/tasks")
def read_tasks():
    return get_tasks()


@app.post("/tasks", status_code=201)
def add_task(task: TaskCreate):
    return create_task(task)


@app.get("/tasks/{task_id}")
def read_task(
    task_id: int = Path(
        ...,
        ge=1,
    )
):
    task = get_task(task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    return task