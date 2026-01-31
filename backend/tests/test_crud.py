import pytest
from starlette.testclient import TestClient
from src.models.task import TaskCreate
from src.api.schemas.task import Task as TaskSchema


def test_create_task_success(async_client: TestClient):
    """Test successful task creation."""
    # Send title, description, and completed as query parameters since that's how the endpoint expects them
    headers = {
        "Authorization": "Bearer mock_token"
    }

    response = async_client.post(
        "/signup/users/from-token/tasks?title=Test Task&description=This is a test task&completed=false",
        headers=headers
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "This is a test task"


def test_create_task_validation_error(async_client: TestClient):
    """Test task creation with invalid data."""
    headers = {
        "Authorization": "Bearer mock_token"
    }

    response = async_client.post(
        "/signup/users/from-token/tasks?title=&description=This is a test task&completed=false",
        headers=headers
    )

    assert response.status_code == 400  # Bad request due to validation error


def test_get_tasks_for_user(async_client: TestClient):
    """Test retrieving tasks for a user."""
    # First create a task
    headers = {
        "Authorization": "Bearer mock_token"
    }

    async_client.post(
        "/signup/users/from-token/tasks?title=Test Task&description=This is a test task&completed=false",
        headers=headers
    )

    # Now get the tasks for the user
    response = async_client.get(
        "/signup/users/from-token/tasks",
        headers=headers
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert any(task["title"] == "Test Task" for task in data)


def test_update_task(async_client: TestClient):
    """Test updating a task."""
    # First create a task
    headers = {
        "Authorization": "Bearer mock_token"
    }

    create_response = async_client.post(
        "/signup/users/from-token/tasks?title=Original Task&description=This is the original task&completed=false",
        headers=headers
    )

    assert create_response.status_code == 201
    created_task = create_response.json()
    task_id = created_task["id"]

    # Now update the task
    update_data = {
        "title": "Updated Task",
        "description": "This is the updated task",
        "completed": True
    }

    update_response = async_client.put(
        f"/signup/users/from-token/tasks/{task_id}",
        json=update_data,
        headers=headers
    )

    assert update_response.status_code == 200
    updated_task = update_response.json()
    assert updated_task["title"] == "Updated Task"
    assert updated_task["completed"] is True


def test_delete_task(async_client: TestClient):
    """Test deleting a task."""
    # First create a task
    headers = {
        "Authorization": "Bearer mock_token"
    }

    create_response = async_client.post(
        "/signup/users/from-token/tasks?title=Task to Delete&description=This task will be deleted&completed=false",
        headers=headers
    )

    assert create_response.status_code == 201
    created_task = create_response.json()
    task_id = created_task["id"]

    # Now delete the task
    delete_response = async_client.delete(
        f"/signup/users/from-token/tasks/{task_id}",
        headers=headers
    )

    assert delete_response.status_code == 204

    # Verify the task is gone by getting all tasks and ensuring it's not there
    get_response = async_client.get(
        f"/signup/users/from-token/tasks",
        headers=headers
    )

    assert get_response.status_code == 200
    tasks = get_response.json()
    assert not any(task["id"] == task_id for task in tasks)


def test_toggle_task_completion(async_client: TestClient):
    """Test toggling task completion status."""
    # First create a task
    headers = {
        "Authorization": "Bearer mock_token"
    }

    create_response = async_client.post(
        "/signup/users/from-token/tasks?title=Task to Toggle&description=This task completion will be toggled&completed=false",
        headers=headers
    )

    assert create_response.status_code == 201
    created_task = create_response.json()
    task_id = created_task["id"]
    assert created_task["completed"] is False

    # Now toggle the completion status
    toggle_data = {"completed": True}
    toggle_response = async_client.patch(
        f"/signup/users/from-token/tasks/{task_id}/complete",
        json=toggle_data,
        headers=headers
    )

    assert toggle_response.status_code == 200
    toggled_task = toggle_response.json()
    assert toggled_task["completed"] is True