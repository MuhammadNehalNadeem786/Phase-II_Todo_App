# Research Findings: Backend Core & Data Layer (FastAPI + Database)

**Date**: 2026-01-16
**Feature**: 1-backend-todo

## Database Connection Configuration

### Decision: Neon PostgreSQL Connection Setup
Using standard SQLModel/SQLAlchemy patterns with connection pooling for Neon Serverless PostgreSQL.

### Rationale:
- Neon's serverless nature benefits from connection pooling
- Standard SQLAlchemy async engine patterns work well with FastAPI
- Connection string follows standard PostgreSQL format

### Implementation Pattern:
```python
from sqlmodel import create_engine
from sqlalchemy.ext.asyncio import create_async_engine

DATABASE_URL = "postgresql+asyncpg://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require"

engine = create_async_engine(DATABASE_URL)
```

### Alternatives Considered:
- Synchronous connections (rejected - FastAPI is async-first)
- Connection string without SSL (rejected - Neon requires SSL)

## Task Model Field Types and Constraints

### Decision: Task Model Schema
Standard SQLModel approach with appropriate field types and validation.

### Rationale:
- SQLModel provides Pydantic validation with SQLAlchemy ORM features
- Auto-generated IDs for primary keys
- Timestamps for audit trail
- Boolean for completion status

### Model Definition:
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
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
```

### Alternatives Considered:
- Different field naming conventions (standard SQLModel approach chosen)
- UUID primary keys (integer auto-increment chosen for simplicity)

## API Endpoint Structure

### Decision: RESTful URL Patterns
Using `/signup/users/{user_id}/tasks/{task_id}` pattern with user_id in the path.

### Rationale:
- Clear indication of user-specific data
- Standard REST convention
- Enables easy user-based filtering
- Complies with security requirement to enforce user isolation

### Alternatives Considered:
- JWT-based user identification in headers only (rejected - path parameter provides clarity and additional security)
- Different versioning scheme (v1 in path chosen as standard practice)

## Error Handling Patterns

### Decision: Standard FastAPI Error Responses
Using HTTPException with standard error formats.

### Rationale:
- FastAPI's built-in HTTPException works well with Pydantic models
- Standard HTTP status codes understood by clients
- Consistent error format for all endpoints

### Implementation Pattern:
```python
from fastapi import HTTPException

def raise_not_found():
    raise HTTPException(status_code=404, detail="Item not found")

def raise_forbidden():
    raise HTTPException(status_code=403, detail="Access denied")
```

### Alternatives Considered:
- Custom exception handlers (standard HTTPException chosen for simplicity)
- Different error response structures (standard format chosen for consistency)

## Security Implementation

### Decision: Query-Level Filtering
Filter all database queries by user_id to enforce data isolation.

### Rationale:
- Most secure approach - data never leaves database with unauthorized access
- Cannot be bypassed by forgetting middleware
- Works consistently across all operations
- Complies with constitution requirement

### Implementation Pattern:
```python
def get_user_tasks(user_id: str, session: Session):
    return session.query(Task).filter(Task.user_id == user_id).all()

def get_task_by_id(task_id: int, user_id: str, session: Session):
    return session.query(Task).filter(
        Task.id == task_id,
        Task.user_id == user_id
    ).first()
```

### Alternatives Considered:
- Middleware-based filtering (rejected - query-level is more secure)
- Service-layer filtering only (rejected - query-level is more robust)