from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from typing import Optional
from src.models.task import Task, TaskCreate
from src.api.schemas.task import Task as TaskSchema


def validate_task_creation(task_create: TaskCreate) -> None:
    """
    Validate task creation data.

    Args:
        task_create: Task creation data to validate

    Raises:
        ValueError: If validation fails
    """
    # Validate title length
    if len(task_create.title) < 1 or len(task_create.title) > 255:
        raise ValueError("Title must be between 1 and 255 characters")

    # Validate description length if provided
    if task_create.description and len(task_create.description) > 1000:
        raise ValueError("Description must not exceed 1000 characters")

    # Validate user_id is not empty
    if not task_create.user_id or len(task_create.user_id.strip()) == 0:
        raise ValueError("User ID cannot be empty")


async def create_task(session: AsyncSession, task_create: TaskCreate) -> Task:
    """
    Create a new task for a user.

    Args:
        session: Database session
        task_create: Task creation data

    Returns:
        Created Task object
    """
    # Validate the task creation data
    validate_task_creation(task_create)

    # Create a Task instance from the TaskCreate data
    db_task = Task(
        title=task_create.title,
        description=task_create.description,
        completed=task_create.completed,
        user_id=task_create.user_id
    )
    session.add(db_task)
    await session.commit()
    await session.refresh(db_task)
    return db_task


async def get_task_by_id(session: AsyncSession, task_id: int, user_id: str) -> Optional[Task]:
    """
    Get a specific task by ID for a user.

    Args:
        session: Database session
        task_id: ID of the task to retrieve
        user_id: ID of the user who owns the task

    Returns:
        Task object if found and owned by user, None otherwise
    """
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    result = await session.execute(statement)
    return result.scalar_one_or_none()


async def get_tasks_by_user(session: AsyncSession, user_id: str) -> list[Task]:
    """
    Get all tasks for a specific user.

    Args:
        session: Database session
        user_id: ID of the user whose tasks to retrieve

    Returns:
        List of Task objects belonging to the user
    """
    statement = select(Task).where(Task.user_id == user_id)
    result = await session.execute(statement)
    return result.scalars().all()


def validate_task_update(task_update: dict) -> None:
    """
    Validate task update data.

    Args:
        task_update: Task update data to validate

    Raises:
        ValueError: If validation fails
    """
    # Validate title if provided
    if "title" in task_update and task_update["title"] is not None:
        title = task_update["title"]
        if len(title) < 1 or len(title) > 255:
            raise ValueError("Title must be between 1 and 255 characters")

    # Validate description if provided
    if "description" in task_update and task_update["description"] is not None:
        description = task_update["description"]
        if len(description) > 1000:
            raise ValueError("Description must not exceed 1000 characters")


async def update_task(session: AsyncSession, task_id: int, user_id: str, task_update: dict) -> Optional[Task]:
    """
    Update a specific task for a user.

    Args:
        session: Database session
        task_id: ID of the task to update
        user_id: ID of the user who owns the task
        task_update: Dictionary with fields to update

    Returns:
        Updated Task object if found and owned by user, None otherwise
    """
    db_task = await get_task_by_id(session, task_id, user_id)
    if not db_task:
        return None

    # Validate the task update data
    validate_task_update(task_update)

    for field, value in task_update.items():
        setattr(db_task, field, value)

    await session.commit()
    await session.refresh(db_task)
    return db_task


async def delete_task(session: AsyncSession, task_id: int, user_id: str) -> bool:
    """
    Delete a specific task for a user.

    Args:
        session: Database session
        task_id: ID of the task to delete
        user_id: ID of the user who owns the task

    Returns:
        True if task was deleted, False if not found or not owned by user
    """
    db_task = await get_task_by_id(session, task_id, user_id)
    if not db_task:
        return False

    await session.delete(db_task)
    await session.commit()
    return True


async def toggle_task_completion(session: AsyncSession, task_id: int, user_id: str) -> Optional[Task]:
    """
    Toggle the completion status of a specific task for a user.

    Args:
        session: Database session
        task_id: ID of the task to update
        user_id: ID of the user who owns the task

    Returns:
        Updated Task object if found and owned by user, None otherwise
    """
    db_task = await get_task_by_id(session, task_id, user_id)
    if not db_task:
        return None

    db_task.completed = not db_task.completed
    await session.commit()
    await session.refresh(db_task)
    return db_task