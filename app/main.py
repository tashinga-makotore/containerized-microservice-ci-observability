from fastapi import FastAPI, HTTPException

from app.models import TaskCreate
from app.service import create_task, get_task, get_tasks
app = FastAPI(
    title="OPS Microservice",
    description="A lightweight service for monitoring and managing processing tasks.",
    version="1.0.0",
)


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
        "status": "healthy"
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
def read_task(task_id: int):
    task = get_task(task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    return task