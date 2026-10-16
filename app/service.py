import logging

from app.models import TaskCreate


logger = logging.getLogger(__name__)


tasks = [
    {
        "id": 1,
        "name": "process-logs",
        "status": "running",
    },
    {
        "id": 2,
        "name": "system-scan",
        "status": "complete",
    },
]


def get_tasks():
    return tasks


def create_task(task: TaskCreate):
    next_id = max(
        (existing_task["id"] for existing_task in tasks),
        default=0,
    ) + 1

    new_task = {
        "id": next_id,
        "name": task.name,
        "status": task.status,
    }

    tasks.append(new_task)

    logger.info(
        "Task created: id=%s name=%s status=%s",
        new_task["id"],
        new_task["name"],
        new_task["status"],
    )

    return new_task


def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task

    logger.warning(
        "Task not found: id=%s",
        task_id,
    )

    return None