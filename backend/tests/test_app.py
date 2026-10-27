
from unittest.mock import MagicMock, patch

from app import create_app


def test_home_endpoint():
    app = create_app(testing=True)
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert response.get_json() == {
        "message": "TaskFlow API is running"
    }


@patch("app.get_db_connection")
def test_tasks_endpoint_returns_list(mock_connection):
    connection = MagicMock()
    cursor = MagicMock()
    mock_connection.return_value = connection
    connection.cursor.return_value = cursor
    cursor.fetchall.return_value = []

    app = create_app(testing=True)
    client = app.test_client()

    response = client.get("/api/tasks")

    assert response.status_code == 200
    assert response.get_json() == []
    cursor.execute.assert_called_once()
    cursor.close.assert_called_once()
    connection.close.assert_called_once()


@patch("app.get_db_connection")
def test_create_task(mock_connection):
    connection = MagicMock()
    cursor = MagicMock()
    mock_connection.return_value = connection
    connection.cursor.return_value = cursor
    cursor.lastrowid = 7
    cursor.fetchone.return_value = {
        "id": 7,
        "title": "Finish XP project",
        "description": "Implement the task API",
        "priority": "High",
        "status": "To Do",
        "due_date": None,
        "created_at": None,
    }

    app = create_app(testing=True)
    client = app.test_client()

    response = client.post(
        "/api/tasks",
        json={
            "title": "Finish XP project",
            "description": "Implement the task API",
            "priority": "High",
        },
    )

    assert response.status_code == 201
    assert response.get_json()["title"] == "Finish XP project"
    assert response.get_json()["priority"] == "High"
    assert response.get_json()["status"] == "To Do"
    connection.commit.assert_called_once()


@patch("app.get_db_connection")
def test_create_task_requires_title(mock_connection):
    app = create_app(testing=True)
    client = app.test_client()

    response = client.post(
        "/api/tasks",
        json={"description": "A task without a title"},
    )

    assert response.status_code == 400
    assert "error" in response.get_json()
    mock_connection.assert_not_called()

@patch("app.get_db_connection")
def test_update_task(mock_connection):
    connection = MagicMock()
    cursor = MagicMock()
    mock_connection.return_value = connection
    connection.cursor.return_value = cursor
    cursor.rowcount = 1

    app = create_app(testing=True)
    client = app.test_client()

    response = client.put(
        "/api/tasks/7",
        json={"status": "Done"}
    )

    assert response.status_code == 200
    connection.commit.assert_called_once()
    cursor.close.assert_called_once()
    connection.close.assert_called_once()


@patch("app.get_db_connection")
def test_update_task_rejects_invalid_status(mock_connection):
    app = create_app(testing=True)
    client = app.test_client()

    response = client.put(
        "/api/tasks/7",
        json={"status": "Invalid Status"}
    )

    assert response.status_code == 400
    mock_connection.assert_not_called()


@patch("app.get_db_connection")
def test_delete_task(mock_connection):
    connection = MagicMock()
    cursor = MagicMock()
    mock_connection.return_value = connection
    connection.cursor.return_value = cursor
    cursor.rowcount = 1

    app = create_app(testing=True)
    client = app.test_client()

    response = client.delete("/api/tasks/7")

    assert response.status_code == 200
    connection.commit.assert_called_once()
    cursor.close.assert_called_once()
    connection.close.assert_called_once()


@patch("app.get_db_connection")
def test_delete_missing_task(mock_connection):
    connection = MagicMock()
    cursor = MagicMock()
    mock_connection.return_value = connection
    connection.cursor.return_value = cursor
    cursor.rowcount = 0

    app = create_app(testing=True)
    client = app.test_client()

    response = client.delete("/api/tasks/99999")

    assert response.status_code == 404
    connection.rollback.assert_called_once()
    cursor.close.assert_called_once()
    connection.close.assert_called_once()
