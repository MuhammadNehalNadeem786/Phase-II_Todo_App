# API Contracts: Authentication & Security Integration

## Authentication API Contract

### JWT Token Structure
```
{
  "userId": "string",
  "email": "string",
  "iat": "number",
  "exp": "number"
}
```

### Authorization Header Format
```
Authorization: Bearer <jwt_token>
```

## Protected Endpoints Contract

### Create Task
- **Method**: POST
- **Path**: `/signup/users/{user_id}/tasks`
- **Headers**:
  - `Authorization: Bearer <valid_jwt>`
  - `Content-Type: application/json`
- **Request Body**: TaskCreate schema with user_id matching authenticated user
- **Responses**:
  - `201 Created`: Task successfully created
  - `401 Unauthorized`: Invalid or missing JWT
  - `403 Forbidden`: User ID mismatch
  - `400 Bad Request`: Invalid request data

### Get User Tasks
- **Method**: GET
- **Path**: `/signup/users/{user_id}/tasks`
- **Headers**: `Authorization: Bearer <valid_jwt>`
- **Responses**:
  - `200 OK`: Array of user's tasks
  - `401 Unauthorized`: Invalid or missing JWT
  - `403 Forbidden`: User ID mismatch

### Get Specific Task
- **Method**: GET
- **Path**: `/signup/users/{user_id}/tasks/{task_id}`
- **Headers**: `Authorization: Bearer <valid_jwt>`
- **Responses**:
  - `200 OK`: Task object
  - `401 Unauthorized`: Invalid or missing JWT
  - `403 Forbidden`: User ID mismatch
  - `404 Not Found`: Task not found

### Update Task
- **Method**: PUT
- **Path**: `/signup/users/{user_id}/tasks/{task_id}`
- **Headers**: `Authorization: Bearer <valid_jwt>`
- **Request Body**: TaskUpdate schema
- **Responses**:
  - `200 OK`: Updated task object
  - `401 Unauthorized`: Invalid or missing JWT
  - `403 Forbidden`: User ID mismatch
  - `404 Not Found`: Task not found

### Delete Task
- **Method**: DELETE
- **Path**: `/signup/users/{user_id}/tasks/{task_id}`
- **Headers**: `Authorization: Bearer <valid_jwt>`
- **Responses**:
  - `204 No Content`: Task successfully deleted
  - `401 Unauthorized`: Invalid or missing JWT
  - `403 Forbidden`: User ID mismatch
  - `404 Not Found`: Task not found

### Toggle Task Completion
- **Method**: PATCH
- **Path**: `/signup/users/{user_id}/tasks/{task_id}/complete`
- **Headers**: `Authorization: Bearer <valid_jwt>`
- **Request Body**: `{ "completed": boolean }`
- **Responses**:
  - `200 OK`: Updated task object
  - `401 Unauthorized`: Invalid or missing JWT
  - `403 Forbidden`: User ID mismatch
  - `404 Not Found`: Task not found

## Error Response Contract

### 401 Unauthorized
```json
{
  "detail": "Invalid token",
  "status_code": 401
}
```

### 403 Forbidden
```json
{
  "detail": "Access denied: Insufficient permissions",
  "status_code": 403
}
```

## Security Requirements
- All endpoints require valid JWT in Authorization header
- User ID in path must match authenticated user ID from JWT
- Request body user_id must match authenticated user_id
- Cross-user access attempts must return 403 Forbidden