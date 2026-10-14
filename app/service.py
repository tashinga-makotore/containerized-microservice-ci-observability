from app.models import TaskCreate


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
    new_task = {
        "id": len(tasks) + 1,
        "name": task.name,
        "status": task.status,
    }

    tasks.append(new_task)

    return new_task


def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task

    return None