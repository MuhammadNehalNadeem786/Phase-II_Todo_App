from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from src.services.task_service import get_tasks_by_user, create_task, get_task_by_id, update_task, delete_task, toggle_task_completion
from src.models.task import TaskCreate
from src.api.schemas.task import Task, TaskUpdate
from src.api.deps.auth import get_current_user_id
from src.models.database import get_async_session

router = APIRouter()


@router.get("/users/from-token/tasks", response_model=List[Task])
async def get_tasks_from_signup_token(
    current_user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Get tasks for the user identified from the signup token (or current session).
    This endpoint is designed to match frontend expectations during the signup flow.

    Args:
        current_user_id: ID of the authenticated user (from JWT)
        session: Database session

    Returns:
        List of tasks belonging to the authenticated user
    """
    tasks = await get_tasks_by_user(session, current_user_id)
    return tasks


@router.post("/users/from-token/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_task_from_signup_token(
    task_request: dict,
    current_user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Create a new task for the user identified from the signup token (or current session).
    This endpoint is designed to match frontend expectations during the signup flow.

    Args:
        task_request: Task creation data (JSON request body)
        current_user_id: ID of the authenticated user (from JWT)
        session: Database session

    Returns:
        Created task
    """
    # Validate required fields
    if "title" not in task_request:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Request body must contain 'title' field"
        )

    # Override user_id to ensure data isolation - always use the authenticated user's ID
    task_data = {
        "title": task_request.get("title"),
        "description": task_request.get("description"),
        "completed": task_request.get("completed", False),
        "user_id": current_user_id
    }

    # Create TaskCreate object with the authenticated user's ID
    validated_task_create = TaskCreate(**task_data)

    try:
        created_task = await create_task(session, validated_task_create)
        return created_task
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/users/from-token/tasks/{task_id}", response_model=Task)
async def update_task_from_signup_token(
    task_id: int,
    task_update: TaskUpdate,
    current_user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Update a specific task for the user identified from the signup token (or current session).
    This endpoint is designed to match frontend expectations during the signup flow.

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


@router.delete("/users/from-token/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task_from_signup_token(
    task_id: int,
    current_user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Delete a specific task for the user identified from the signup token (or current session).
    This endpoint is designed to match frontend expectations during the signup flow.

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


@router.patch("/users/from-token/tasks/{task_id}/complete", response_model=Task)
async def toggle_task_completion_from_signup_token(
    task_id: int,
    request_data: dict,
    current_user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Toggle completion status of a specific task for the user identified from the signup token (or current session).
    This endpoint is designed to match frontend expectations during the signup flow.

    Args:
        task_id: ID of the task to update
        request_data: Dict containing completion status
        current_user_id: ID of the authenticated user (from JWT)
        session: Database session

    Returns:
        Updated task with new completion status
    """
    if "completed" not in request_data:
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