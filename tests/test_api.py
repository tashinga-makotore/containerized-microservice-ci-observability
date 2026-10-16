import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.service import tasks


client = TestClient(app)


INITIAL_TASKS = [
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


@pytest.fixture(autouse=True)
def reset_tasks():
    tasks.clear()
    tasks.extend(task.copy() for task in INITIAL_TASKS)

    yield

    tasks.clear()
    tasks.extend(task.copy() for task in INITIAL_TASKS)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["service"] == "OPS Microservice"
    assert response.json()["status"] == "online"


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy"
    }


def test_status():
    response = client.get("/status")

    assert response.status_code == 200
    assert response.json()["status"] == "operational"


def test_get_tasks():
    response = client.get("/tasks")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["name"] == "process-logs"


def test_create_task():
    new_task = {
        "name": "telemetry-export",
        "status": "pending",
    }

    response = client.post(
        "/tasks",
        json=new_task,
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == 3
    assert data["name"] == "telemetry-export"
    assert data["status"] == "pending"


def test_default_task_status():
    response = client.post(
        "/tasks",
        json={
            "name": "network-scan",
        },
    )

    assert response.status_code == 201
    assert response.json()["status"] == "pending"


def test_invalid_status():
    response = client.post(
        "/tasks",
        json={
            "name": "telemetry-export",
            "status": "banana",
        },
    )

    assert response.status_code == 422


def test_invalid_task_name():
    response = client.post(
        "/tasks",
        json={
            "name": " ",
            "status": "pending",
        },
    )

    assert response.status_code == 422


def test_get_existing_task():
    response = client.get("/tasks/1")

    assert response.status_code == 200
    assert response.json()["name"] == "process-logs"


def test_missing_task():
    response = client.get("/tasks/999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Task not found"
    }


def test_invalid_task_id():
    response = client.get("/tasks/0")

    assert response.status_code == 422