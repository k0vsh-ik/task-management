import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

Base.metadata.create_all(bind=engine)

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def create_sample_task():
    response = client.post(
        "/api/tasks",
        json={"title": "Test Task", "description": "Test Description", "status": "To Do"}
    )
    return response.json()


def test_create_task():
    response = client.post(
        "/api/tasks",
        json={"title": "New Task", "description": "Description", "status": "To Do"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New Task"
    assert data["status"] == "To Do"


def test_create_task_invalid_status():
    response = client.post(
        "/api/tasks",
        json={"title": "Invalid", "description": "Bad", "status": "Invalid Status"}
    )
    assert response.status_code == 422 or response.status_code == 400


def test_list_tasks():
    create_sample_task()
    response = client.get("/api/tasks")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert isinstance(data["tasks"], list)
    assert data["total"] is not None


def test_list_tasks_with_wrong_filter():
    create_sample_task()
    response = client.get("/api/tasks?status=To Do")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] is not None

    response = client.get("/api/tasks?status=Invalid")
    assert response.status_code == 400


def test_list_tasks_with_filter():
    create_sample_task()
    response = client.get("/api/tasks?status=To Do")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] is not None

    response = client.get("/api/tasks?status=In Progress")
    assert response.status_code == 200


def test_update_task():
    task = create_sample_task()
    task_id = task["id"]

    response = client.put(
        f"/api/tasks/{task_id}",
        json={"title": "Updated Title"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"


def test_update_task_not_found():
    response = client.put(
        "/api/tasks/999",
        json={"title": "Does Not Exist"}
    )
    assert response.status_code == 404


def test_delete_task():
    task = create_sample_task()
    task_id = task["id"]

    response = client.delete(f"/api/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["detail"] == "Task deleted"


def test_delete_task_not_found():
    response = client.delete("/api/tasks/999")
    assert response.status_code == 404
