from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from src.services.task_service import (
    create_task, get_task_by_id, get_tasks_by_user,
    update_task, delete_task, toggle_task_completion, validate_task_creation
)
from src.models.task import TaskCreate
from src.api.schemas.task import Task, TaskUpdate
from src.api.schemas.errors import NotFoundResponse, ForbiddenResponse
from src.models.database import get_async_session
from src.api.deps.auth import get_current_user_id, verify_user_access

router = APIRouter()


@router.get("/users/me/tasks", response_model=List[Task])
async def get_current_user_tasks(
    current_user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Get all tasks for the currently authenticated user (extracted from JWT).

    Args:
        current_user_id: ID of the authenticated user (from JWT)
        session: Database session

    Returns:
        List of tasks belonging to the authenticated user
    """
    tasks = await get_tasks_by_user(session, current_user_id)
    return tasks


@router.post("/users/me/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_current_user_task(
    title: str,
    description: str = None,
    completed: bool = False,
    current_user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Create a new task for the currently authenticated user (extracted from JWT).

    Args:
        title: Task title
        description: Task description (optional)
        completed: Whether task is completed (default: False)
        current_user_id: ID of the authenticated user (from JWT)
        session: Database session

    Returns:
        Created task
    """
    # Create TaskCreate object with the authenticated user's ID
    task_create = TaskCreate(
        title=title,
        description=description,
        completed=completed,
        user_id=current_user_id
    )

    try:
        created_task = await create_task(session, task_create)
        return created_task
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/users/{user_id}/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_task_endpoint(
    user_id: str,
    task_create: TaskCreate,
    current_user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Create a new task for a user.

    Args:
        user_id: ID of the user creating the task
        task_create: Task creation data
        current_user_id: ID of the authenticated user (from JWT)
        session: Database session

    Returns:
        Created task
    """
    # Verify that the user_id in the path matches the authenticated user_id
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User ID in path does not match authenticated user"
        )

    # Also verify that the user_id in the task data matches the authenticated user
    if task_create.user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User ID in request body does not match authenticated user"
        )

    try:
        created_task = await create_task(session, task_create)
        return created_task
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/users/{user_id}/tasks", response_model=List[Task])
async def get_tasks_for_user(
    user_id: str,
    current_user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Get all tasks for a specific user.

    Args:
        user_id: ID of the user whose tasks to retrieve
        current_user_id: ID of the authenticated user (from JWT)
        session: Database session

    Returns:
        List of tasks belonging to the user
    """
    # Verify that the user_id in the path matches the authenticated user_id
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User ID in path does not match authenticated user"
        )

    tasks = await get_tasks_by_user(session, user_id)
    return tasks


@router.put("/users/me/tasks/{task_id}", response_model=Task)
async def update_current_user_task(
    task_id: int,
    task_update: TaskUpdate,
    current_user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Update a specific task for the currently authenticated user (extracted from JWT).

    Args:
        task_id: ID of the task to update
        task_update: Task update data
        current_user_id: ID of the authenticated user (from JWT)
        session: Database session

    Returns:
        Updated task
    """
    # Convert TaskUpdate to dict, excluding unset values
    update_data = task_update.dict(exclude_unset=True)

    try:
        updated_task = await update_task(session, task_id, current_user_id, update_data)
        if not updated_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        return updated_task
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/users/me/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_current_user_task(
    task_id: int,
    current_user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Delete a specific task for the currently authenticated user (extracted from JWT).

    Args:
        task_id: ID of the task to delete
        current_user_id: ID of the authenticated user (from JWT)
        session: Database session
    """
    deleted = await delete_task(session, task_id, current_user_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )


@router.patch("/users/me/tasks/{task_id}/complete", response_model=Task)
async def toggle_current_user_task_completion(
    task_id: int,
    completed: dict,
    current_user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Toggle completion status of a specific task for the currently authenticated user (extracted from JWT).

    Args:
        task_id: ID of the task to update
        completed: Dict containing completion status
        current_user_id: ID of the authenticated user (from JWT)
        session: Database session

    Returns:
        Updated task with new completion status
    """
    if "completed" not in completed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Request body must contain 'completed' field"
        )

    task = await get_task_by_id(session, task_id, current_user_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Update the completion status
    updated_task = await toggle_task_completion(session, task_id, current_user_id)
    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return updated_task


@router.get("/users/{user_id}/tasks/{task_id}", response_model=Task)
async def get_single_task(
    user_id: str,
    task_id: int,
    current_user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Get a specific task for a user.

    Args:
        user_id: ID of the user whose task to retrieve
        task_id: ID of the task to retrieve
        current_user_id: ID of the authenticated user (from JWT)
        session: Database session

    Returns:
        Task details
    """
    # Verify that the user_id in the path matches the authenticated user_id
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User ID in path does not match authenticated user"
        )

    task = await get_task_by_id(session, task_id, user_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task


@router.put("/users/{user_id}/tasks/{task_id}", response_model=Task)
async def update_task_endpoint(
    user_id: str,
    task_id: int,
    task_update: TaskUpdate,
    current_user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Update a specific task for a user.

    Args:
        user_id: ID of the user whose task to update
        task_id: ID of the task to update
        task_update: Task update data
        current_user_id: ID of the authenticated user (from JWT)
        session: Database session

    Returns:
        Updated task
    """
    # Verify that the user_id in the path matches the authenticated user_id
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User ID in path does not match authenticated user"
        )

    # Convert TaskUpdate to dict, excluding unset values
    update_data = task_update.dict(exclude_unset=True)

    try:
        updated_task = await update_task(session, task_id, user_id, update_data)
        if not updated_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        return updated_task
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/users/{user_id}/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task_endpoint(
    user_id: str,
    task_id: int,
    current_user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Delete a specific task for a user.

    Args:
        user_id: ID of the user whose task to delete
        task_id: ID of the task to delete
        current_user_id: ID of the authenticated user (from JWT)
        session: Database session
    """
    # Verify that the user_id in the path matches the authenticated user_id
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User ID in path does not match authenticated user"
        )

    deleted = await delete_task(session, task_id, user_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )


@router.patch("/users/{user_id}/tasks/{task_id}/complete", response_model=Task)
async def toggle_task_completion_endpoint(
    user_id: str,
    task_id: int,
    completed: dict,
    current_user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Toggle completion status of a specific task for a user.

    Args:
        user_id: ID of the user whose task to update
        task_id: ID of the task to update
        completed: Dict containing completion status
        current_user_id: ID of the authenticated user (from JWT)
        session: Database session

    Returns:
        Updated task with new completion status
    """
    # Verify that the user_id in the path matches the authenticated user_id
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User ID in path does not match authenticated user"
        )

    if "completed" not in completed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Request body must contain 'completed' field"
        )

    task = await get_task_by_id(session, task_id, user_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Update the completion status
    updated_task = await toggle_task_completion(session, task_id, user_id)
    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return updated_task