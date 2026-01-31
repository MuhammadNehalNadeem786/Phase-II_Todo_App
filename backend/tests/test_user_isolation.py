import pytest
from httpx import AsyncClient
from src.models.task import TaskCreate


@pytest.mark.asyncio
async def test_user_isolation_get_tasks(async_client: AsyncClient):
    """Test that users can only access their own tasks."""
    headers_user1 = {
        "Authorization": "Bearer mock_token_user1",
        "Content-Type": "application/json"
    }

    headers_user2 = {
        "Authorization": "Bearer mock_token_user2",
        "Content-Type": "application/json"
    }

    # Create tasks for user1
    task_data_user1 = {
        "title": "User1 Task",
        "description": "Task for user1",
        "completed": False,
        "user_id": "user1"
    }

    response1 = await async_client.post(
        "/signup/users/user1/tasks",
        json=task_data_user1,
        headers=headers_user1
    )

    assert response1.status_code == 201

    # Create tasks for user2
    task_data_user2 = {
        "title": "User2 Task",
        "description": "Task for user2",
        "completed": False,
        "user_id": "user2"
    }

    response2 = await async_client.post(
        "/signup/users/user2/tasks",
        json=task_data_user2,
        headers=headers_user2
    )

    assert response2.status_code == 201

    # User1 should only see their own tasks
    get_user1_tasks = await async_client.get(
        "/signup/users/user1/tasks",
        headers=headers_user1
    )

    assert get_user1_tasks.status_code == 200
    user1_tasks = get_user1_tasks.json()
    assert len(user1_tasks) == 1
    assert user1_tasks[0]["title"] == "User1 Task"

    # User2 should only see their own tasks
    get_user2_tasks = await async_client.get(
        "/signup/users/user2/tasks",
        headers=headers_user2
    )

    assert get_user2_tasks.status_code == 200
    user2_tasks = get_user2_tasks.json()
    assert len(user2_tasks) == 1
    assert user2_tasks[0]["title"] == "User2 Task"


@pytest.mark.asyncio
async def test_user_cannot_access_other_users_tasks(async_client: AsyncClient):
    """Test that a user cannot access another user's tasks."""
    headers_user1 = {
        "Authorization": "Bearer mock_token_user1",
        "Content-Type": "application/json"
    }

    headers_user2 = {
        "Authorization": "Bearer mock_token_user2",
        "Content-Type": "application/json"
    }

    # Create a task for user1
    task_data = {
        "title": "Private Task",
        "description": "This is user1's private task",
        "completed": False,
        "user_id": "user1"
    }

    create_response = await async_client.post(
        "/signup/users/user1/tasks",
        json=task_data,
        headers=headers_user1
    )

    assert create_response.status_code == 201
    created_task = create_response.json()
    task_id = created_task["id"]

    # User2 should not be able to access user1's task
    get_response = await async_client.get(
        f"/signup/users/user1/tasks/{task_id}",
        headers=headers_user2  # User2 trying to access user1's task
    )

    # This should fail with a 403 Forbidden or 404 Not Found depending on implementation
    assert get_response.status_code in [403, 404]


@pytest.mark.asyncio
async def test_user_cannot_modify_other_users_tasks(async_client: AsyncClient):
    """Test that a user cannot modify another user's tasks."""
    headers_user1 = {
        "Authorization": "Bearer mock_token_user1",
        "Content-Type": "application/json"
    }

    headers_user2 = {
        "Authorization": "Bearer mock_token_user2",
        "Content-Type": "application/json"
    }

    # Create a task for user1
    task_data = {
        "title": "Protected Task",
        "description": "This is user1's protected task",
        "completed": False,
        "user_id": "user1"
    }

    create_response = await async_client.post(
        "/signup/users/user1/tasks",
        json=task_data,
        headers=headers_user1
    )

    assert create_response.status_code == 201
    created_task = create_response.json()
    task_id = created_task["id"]

    # User2 should not be able to update user1's task
    update_data = {
        "title": "Hacked Task",
        "completed": True
    }

    update_response = await async_client.put(
        f"/signup/users/user1/tasks/{task_id}",
        json=update_data,
        headers=headers_user2  # User2 trying to update user1's task
    )

    assert update_response.status_code in [403, 404]

    # User2 should not be able to delete user1's task
    delete_response = await async_client.delete(
        f"/signup/users/user1/tasks/{task_id}",
        headers=headers_user2  # User2 trying to delete user1's task
    )

    assert delete_response.status_code in [403, 404]