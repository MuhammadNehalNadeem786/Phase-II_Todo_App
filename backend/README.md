# Todo Backend API

A FastAPI-based backend with SQLModel ORM and Neon Serverless PostgreSQL for persistent task storage. The system enforces user-based data isolation at the query level to ensure each user can only access their own tasks.

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
ENVIRONMENT=development
```

### 4. Initialize Database
Run database migrations to create the tasks table:
```bash
# If using alembic for migrations
alembic upgrade head

# Or if using SQLModel's table creation
python -c "from src.models.database import create_db_and_tables; create_db_and_tables()"
```

### 5. Start the Development Server
```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
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


## Deployment Instructions

### Docker Deployment

1. Create a `Dockerfile` in the project root:

```Dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

2. Build and run the Docker container:

```bash
docker build -t todo-backend .
docker run -d -p 8000:8000 --env-file .env todo-backend
```

### Production Deployment

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables in production:
```bash
export DATABASE_URL="postgresql+asyncpg://..."
export BETTER_AUTH_SECRET="your-production-secret"
export ENVIRONMENT="production"
export LOG_LEVEL="WARNING"
```

3. Run database migrations:
```bash
alembic upgrade head
```

4. Deploy using a WSGI/ASGI server like Gunicorn/Uvicorn:
```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Environment Configuration

Create a `.env` file with appropriate values for your environment:

```env
DATABASE_URL=postgresql+asyncpg://username:password@host:port/database?sslmode=require
BETTER_AUTH_SECRET=your-production-jwt-secret
ENVIRONMENT=production
LOG_LEVEL=INFO
```

### Health Checks

The application provides a health check endpoint at `/health` which returns a 200 status when the service is operational.


## Database Setup & Initialization

### Setting up Neon PostgreSQL

1. Create a Neon PostgreSQL project at [neon.tech](https://neon.tech)
2. Get your connection string from the Neon dashboard
3. Update your `.env` file with the connection string:

```env
DATABASE_URL=postgresql+asyncpg://username:password@ep-xxxxxx.us-east-1.aws.neon.tech/dbname?sslmode=require
```

### Initializing the Database

#### Option 1: Using the initialization script (Recommended)
```bash
cd backend
python src/db_init.py
```

#### Option 2: Using Alembic for migrations
```bash
# Generate initial migration
alembic revision --autogenerate -m "Initial migration"

# Apply the migration
alembic upgrade head
```

#### Option 3: Direct table creation
```bash
python -c "from src.models.database import init_db; init_db()"
```

### Running the Application

To run the application with automatic database initialization:

```bash
cd backend
python start_server.py
```

Or use the convenience script:
```bash
python ../init_db.py  # From the backend directory
```


The backend stack is a FastAPI app using SQLModel, asyncpg, Alembic, and Uvicorn, with configuration via a .env file. I have created a production-ready Dockerfile and a .dockerignore for your backend in backend/.

To build and push your backend image to Docker Hub:

Open a terminal in backend/:
Build the Docker image (replace <your-dockerhub-username> as needed):
docker build -t <your-dockerhub-username>/todo-backend:latest .
Log in to Docker Hub: docker login
Push the image: docker push <your-dockerhub-username>/todo-backend:latest
Your backend is now ready for containerized deployment and distribution via Docker Hub. Let me know if you want a docker-compose setup or further automation!