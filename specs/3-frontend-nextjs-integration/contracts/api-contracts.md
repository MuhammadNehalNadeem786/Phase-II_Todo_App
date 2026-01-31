# API Contracts: Frontend Application & Full-Stack Integration

## Authentication API Contracts

### Login Endpoint
- **Method**: POST
- **Path**: `/api/login` (or handled by Better Auth)
- **Headers**:
  - `Content-Type: application/json`
- **Request Body**:
  ```json
  {
    "email": "string",
    "password": "string"
  }
  ```
- **Successful Response**: 200 OK
  ```json
  {
    "user": {
      "id": "string",
      "email": "string"
    },
    "token": "jwt_token_string"
  }
  ```
- **Error Responses**:
  - 400: Invalid credentials format
  - 401: Invalid username/password
  - 500: Server error

### Signup Endpoint
- **Method**: POST
- **Path**: `/api/signup` (or handled by Better Auth)
- **Headers**:
  - `Content-Type: application/json`
- **Request Body**:
  ```json
  {
    "email": "string",
    "password": "string",
    "confirmPassword": "string"
  }
  ```
- **Successful Response**: 201 Created
  ```json
  {
    "user": {
      "id": "string",
      "email": "string"
    },
    "token": "jwt_token_string"
  }
  ```
- **Error Responses**:
  - 400: Invalid input format
  - 409: User already exists
  - 500: Server error

### Logout Endpoint
- **Method**: POST
- **Path**: `/api/auth/logout` (or handled by Better Auth)
- **Headers**:
  - `Authorization: Bearer <jwt_token>`
- **Successful Response**: 200 OK
  ```json
  {
    "message": "Successfully logged out"
  }
  ```

## Task Management API Contracts

### Get User Tasks
- **Method**: GET
- **Path**: `/signup/users/{user_id}/tasks`
- **Headers**:
  - `Authorization: Bearer <jwt_token>`
- **Successful Response**: 200 OK
  ```json
  [
    {
      "id": 1,
      "title": "string",
      "description": "string",
      "completed": false,
      "user_id": "string",
      "created_at": "2023-01-01T00:00:00Z",
      "updated_at": "2023-01-01T00:00:00Z"
    }
  ]
  ```
- **Error Responses**:
  - 401: Unauthorized (invalid/missing token)
  - 403: Forbidden (user_id mismatch)
  - 500: Server error

### Create Task
- **Method**: POST
- **Path**: `/signup/users/{user_id}/tasks`
- **Headers**:
  - `Authorization: Bearer <jwt_token>`
  - `Content-Type: application/json`
- **Request Body**:
  ```json
  {
    "title": "string",
    "description": "string",
    "completed": false,
    "user_id": "string"
  }
  ```
- **Successful Response**: 201 Created
  ```json
  {
    "id": 123,
    "title": "string",
    "description": "string",
    "completed": false,
    "user_id": "string",
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-01T00:00:00Z"
  }
  ```
- **Error Responses**:
  - 400: Invalid input data
  - 401: Unauthorized (invalid/missing token)
  - 403: Forbidden (user_id mismatch)
  - 500: Server error

### Get Single Task
- **Method**: GET
- **Path**: `/signup/users/{user_id}/tasks/{task_id}`
- **Headers**:
  - `Authorization: Bearer <jwt_token>`
- **Successful Response**: 200 OK
  ```json
  {
    "id": 123,
    "title": "string",
    "description": "string",
    "completed": false,
    "user_id": "string",
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-01T00:00:00Z"
  }
  ```
- **Error Responses**:
  - 401: Unauthorized (invalid/missing token)
  - 403: Forbidden (user_id mismatch)
  - 404: Task not found
  - 500: Server error

### Update Task
- **Method**: PUT
- **Path**: `/signup/users/{user_id}/tasks/{task_id}`
- **Headers**:
  - `Authorization: Bearer <jwt_token>`
  - `Content-Type: application/json`
- **Request Body**:
  ```json
  {
    "title": "string",
    "description": "string",
    "completed": true
  }
  ```
- **Successful Response**: 200 OK
  ```json
  {
    "id": 123,
    "title": "updated string",
    "description": "updated string",
    "completed": true,
    "user_id": "string",
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-02T00:00:00Z"
  }
  ```
- **Error Responses**:
  - 400: Invalid input data
  - 401: Unauthorized (invalid/missing token)
  - 403: Forbidden (user_id mismatch)
  - 404: Task not found
  - 500: Server error

### Delete Task
- **Method**: DELETE
- **Path**: `/signup/users/{user_id}/tasks/{task_id}`
- **Headers**:
  - `Authorization: Bearer <jwt_token>`
- **Successful Response**: 204 No Content
- **Error Responses**:
  - 401: Unauthorized (invalid/missing token)
  - 403: Forbidden (user_id mismatch)
  - 404: Task not found
  - 500: Server error

### Toggle Task Completion
- **Method**: PATCH
- **Path**: `/signup/users/{user_id}/tasks/{task_id}/complete`
- **Headers**:
  - `Authorization: Bearer <jwt_token>`
  - `Content-Type: application/json`
- **Request Body**:
  ```json
  {
    "completed": true
  }
  ```
- **Successful Response**: 200 OK
  ```json
  {
    "id": 123,
    "title": "string",
    "description": "string",
    "completed": true,
    "user_id": "string",
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-02T00:00:00Z"
  }
  ```
- **Error Responses**:
  - 400: Invalid input data
  - 401: Unauthorized (invalid/missing token)
  - 403: Forbidden (user_id mismatch)
  - 404: Task not found
  - 500: Server error

## Error Response Contract

### 401 Unauthorized
```json
{
  "detail": "Unauthorized - Invalid or expired token",
  "status_code": 401,
  "error_type": "authentication_error"
}
```

### 403 Forbidden
```json
{
  "detail": "Access denied: Insufficient permissions",
  "status_code": 403,
  "error_type": "authorization_error"
}
```

### 400 Bad Request
```json
{
  "detail": "Validation error or bad request",
  "status_code": 400,
  "error_type": "validation_error"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error",
  "status_code": 500,
  "error_type": "server_error"
}
```

## Frontend API Client Contract

### Authorization Header Injection
- All authenticated requests must include:
  - `Authorization: Bearer <jwt_token>`
- Token retrieved from frontend session management
- Token validated for expiration before each request

### Request/Response Interception
- Request interceptor: Add JWT token to all requests
- Response interceptor: Handle 401/403 responses with redirect to login
- Error handling: Transform backend errors to user-friendly messages

### Frontend Caching Strategy
- Cache user's task list with appropriate TTL
- Invalidate cache on mutations (create, update, delete)
- Handle optimistic updates for better UX