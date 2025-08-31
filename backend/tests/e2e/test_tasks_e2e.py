import pytest
import time
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.database import Base, engine

# -----------------------------
# Setup / teardown DB
# -----------------------------
@pytest.fixture(scope="module", autouse=True)
async def setup_db():
    # Создаем таблицы
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Удаляем таблицы после тестов
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

# -----------------------------
# Async HTTP E2E tests
# -----------------------------
@pytest.mark.asyncio
async def test_create_list_update_delete_task():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://testserver"
    ) as client:
        # ---- Create ----
        task_data = {"title": "Task1", "description": "Desc", "status": "To Do"}
        response = await client.post("/api/tasks", json=task_data)
        assert response.status_code == 200
        task = response.json()
        task_id = task["id"]
        assert task["title"] == "Task1"

        # ---- List ----
        response = await client.get("/api/tasks")
        data = response.json()
        assert data["total"] == 1
        assert data["tasks"][0]["id"] == task_id

        # ---- Update ----
        response = await client.put(f"/api/tasks/{task_id}", json={"title": "Updated Task"})
        updated_task = response.json()
        assert updated_task["title"] == "Updated Task"

        # ---- Delete ----
        response = await client.delete(f"/api/tasks/{task_id}")
        assert response.status_code == 200
        assert response.json()["detail"] == "Task deleted"

        # ---- Verify empty ----
        response = await client.get("/api/tasks")
        data = response.json()
        assert data["total"] == 0

# -----------------------------
# WebSocket E2E test (sync)
# -----------------------------
def test_websocket_broadcast():
    with TestClient(app) as client:
        with client.websocket_connect("/ws/tasks") as ws:
            # Создаем задачу через HTTP
            task_data = {"title": "WS Task", "description": "WS Desc", "status": "To Do"}
            resp = client.post("/api/tasks", json=task_data)
            assert resp.status_code == 200

            # Даем серверу время для отправки broadcast
            time.sleep(0.1)

            # Получаем сообщение через WebSocket
            msg = ws.receive_json()
            assert msg["event"] == "created"
            assert msg["task"]["title"] == "WS Task"

            # Закрываем WebSocket
            ws.send_text("close")
            ws.close()
