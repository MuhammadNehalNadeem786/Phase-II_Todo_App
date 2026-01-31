# Quickstart Guide: Backend Core & Data Layer (FastAPI + Database)

**Date**: 2026-01-16
**Feature**: 1-backend-todo

## Prerequisites

- Python 3.9+
- Poetry or pip for dependency management
- Neon Serverless PostgreSQL database instance
- Environment variables configured for database connection

## Setup Instructions

### 1. Clone and Navigate to Project
```bash
git clone <repository-url>
cd <project-directory>
```

### 2. Install Dependencies
Using Poetry:
```bash
poetry install
poetry shell
```

Or using pip:
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a `.env` file with your Neon PostgreSQL connection details:
```env
DATABASE_URL=postgresql+asyncpg://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require
BETTER_AUTH_SECRET=your-jwt-secret-key
```

### 4. Initialize Database
Run database migrations to create the tasks table:
```bash
# If using alembic for migrations
alembic upgrade head

# Or if using SQLModel's table creation
python -c "from app.db import create_db_and_tables; create_db_and_tables()"
```

### 5. Start the Development Server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Usage Examples

### Authentication
All API requests require a valid JWT token in the Authorization header:
```
Authorization: Bearer <jwt-token>
```

### Create a Task
```bash
curl -X POST http://localhost:8000/signup/users/user123/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <jwt-token>" \
  -d '{
    "title": "Complete project documentation",
    "description": "Write comprehensive guides for the new feature",
    "completed": false
  }'
```

### Get All Tasks for a User
```bash
curl -X GET http://localhost:8000/signup/users/user123/tasks \
  -H "Authorization: Bearer <jwt-token>"
```

### Get a Specific Task
```bash
curl -X GET http://localhost:8000/signup/users/user123/tasks/1 \
  -H "Authorization: Bearer <jwt-token>"
```

### Update a Task
```bash
curl -X PUT http://localhost:8000/signup/users/user123/tasks/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <jwt-token>" \
  -d '{
    "title": "Updated task title",
    "description": "Updated description",
    "completed": true
  }'
```

### Delete a Task
```bash
curl -X DELETE http://localhost:8000/signup/users/user123/tasks/1 \
  -H "Authorization: Bearer <jwt-token>"
```

### Toggle Task Completion
```bash
curl -X PATCH http://localhost:8000/signup/users/user123/tasks/1/complete \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <jwt-token>" \
  -d '{"completed": true}'
```

## Key Features

1. **User Isolation**: Each user can only access their own tasks
2. **Persistent Storage**: Tasks are stored in Neon Serverless PostgreSQL
3. **RESTful API**: Standard HTTP methods with predictable endpoints
4. **JSON Responses**: All data exchanged in JSON format
5. **Proper Error Handling**: Standard HTTP status codes for all responses

## Common Issues and Solutions

### Database Connection Issues
- Verify your Neon PostgreSQL connection string is correct
- Check that your database instance is active
- Ensure SSL mode is set to require for Neon

### Authentication Failures
- Confirm your JWT token is valid and not expired
- Verify the token contains the correct user information
- Check that the user_id in the request path matches the authenticated user

### 403 Forbidden Errors
- Ensure the user_id in the URL path matches the authenticated user
- Verify that the task belongs to the authenticated user