# Data Model: Backend Core & Data Layer (FastAPI + Database)

**Date**: 2026-01-16
**Feature**: 1-backend-todo

## Entity: Task

### Attributes

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | Integer | Primary Key, Auto-increment | Unique identifier for each task |
| title | String | Required, Min length: 1, Max length: 255 | The task title or subject |
| description | String | Optional, Max length: 1000 | Detailed description of the task |
| completed | Boolean | Default: False | Completion status of the task |
| user_id | String | Required | Identifier of the user who owns this task |
| created_at | DateTime | Auto-generated | Timestamp when the task was created |
| updated_at | DateTime | Auto-generated | Timestamp when the task was last updated |

### Relationships
- **Owner Relationship**: Each Task belongs to a User (identified by user_id)
- **Cardinality**: Many Tasks to One User (each user can have many tasks)

### Validation Rules
1. `title` must be provided and not empty (length > 0)
2. `title` must not exceed 255 characters
3. `description` can be null/empty but if provided must not exceed 1000 characters
4. `completed` defaults to False when creating a new task
5. `user_id` must match the authenticated user during operations
6. `created_at` is set automatically on creation
7. `updated_at` is set automatically on creation and updates

### State Transitions
- **Creation**: New task with `completed = False`, `created_at` and `updated_at` set to current time
- **Update**: Task properties changed, `updated_at` updated to current time
- **Completion Toggle**: `completed` field toggled, `updated_at` updated to current time
- **Deletion**: Task removed from database

## Entity: User (Reference)

### Attributes
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| user_id | String | Required, Unique | Unique identifier for each user |

### Relationship to Task
- One User to Many Tasks relationship
- All task operations must be filtered by user_id to ensure data isolation

## Database Schema

### Table: tasks
```
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    user_id VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

### Indexes
- Index on `user_id` for efficient user-based queries
- Index on `user_id` and `completed` for filtered queries
- Primary key index on `id`

### Constraints
- NOT NULL constraints on required fields
- Check constraint on title length (1-255 characters)
- Foreign key relationship to users table (conceptual - users table managed separately)

## SQLModel Class Definition

```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    user_id: str

class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

## Query Patterns

### Security Enforcement
All database queries must include user_id filtering to ensure data isolation:

```python
# Correct - filters by user_id
tasks = session.exec(
    select(Task).where(Task.user_id == user_id)
).all()

# Incorrect - could return tasks from other users
tasks = session.exec(select(Task)).all()
```

### Common Operations
- Retrieve all tasks for a user: Filter by user_id
- Retrieve specific task: Filter by task_id AND user_id
- Update task: Verify task belongs to user before updating
- Delete task: Verify task belongs to user before deleting
- Toggle completion: Verify task belongs to user before updating