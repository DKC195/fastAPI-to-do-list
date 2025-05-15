from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_home_page():
    response = client.get("/")
    assert response.status_code == 200
    assert "Todo List" in response.text


def test_add_todo():
    response = client.post(
        "/add",
        data={"title": "Test Task", "description": "Test description"},
        follow_redirects=False,
    )
    assert response.status_code == 303  # Redirect after adding


def test_mark_complete():
    # First, add a todo
    client.post("/add", data={"title": "Temp", "description": ""})
    response = client.post("/complete/1", follow_redirects=False)
    assert response.status_code == 303
