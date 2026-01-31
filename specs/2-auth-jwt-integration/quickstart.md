# Quickstart: Authentication & Security Integration (Better Auth + JWT)

## Prerequisites

- Python 3.11+
- FastAPI
- python-jose[cryptography]
- Better Auth configured on frontend

## Environment Setup

### Backend Configuration
```bash
# In backend/.env
BETTER_AUTH_SECRET="your-production-secret-key"
```

### Frontend Configuration
```bash
# In frontend/.env.local
NEXT_PUBLIC_BETTER_AUTH_SECRET="same-secret-key-as-backend"
NEXT_PUBLIC_API_BASE_URL="http://localhost:8000"
```

## API Usage

### Authentication Flow

1. **User Authentication** (Frontend)
   - User signs in via Better Auth
   - Better Auth issues JWT token

2. **Token Storage** (Frontend)
   - Store JWT securely (httpOnly cookie or secure storage)

3. **Authenticated API Requests** (Frontend)
   ```javascript
   // Automatically include JWT in all requests
   const response = await fetch('/signup/users/{user_id}/tasks', {
     headers: {
       'Authorization': 'Bearer ' + storedToken,
       'Content-Type': 'application/json'
     }
   });
   ```

4. **Token Verification** (Backend)
   - Extract JWT from Authorization header
   - Verify signature with BETTER_AUTH_SECRET
   - Decode user identity
   - Validate user access

## Protected Endpoints

### Create Task
```http
POST /signup/users/{user_id}/tasks
Authorization: Bearer <valid_jwt_token>
Content-Type: application/json

{
  "title": "New task",
  "description": "Task description",
  "completed": false,
  "user_id": "{authenticated_user_id}"
}
```

### Get User Tasks
```http
GET /signup/users/{user_id}/tasks
Authorization: Bearer <valid_jwt_token>
```

### Get Specific Task
```http
GET /signup/users/{user_id}/tasks/{task_id}
Authorization: Bearer <valid_jwt_token>
```

### Update Task
```http
PUT /signup/users/{user_id}/tasks/{task_id}
Authorization: Bearer <valid_jwt_token>
Content-Type: application/json

{
  "title": "Updated task title",
  "description": "Updated description",
  "completed": true
}
```

### Delete Task
```http
DELETE /signup/users/{user_id}/tasks/{task_id}
Authorization: Bearer <valid_jwt_token>
```

### Toggle Task Completion
```http
PATCH /signup/users/{user_id}/tasks/{task_id}/complete
Authorization: Bearer <valid_jwt_token>
Content-Type: application/json

{
  "completed": true
}
```

## Error Handling

### 401 Unauthorized Responses
- Missing Authorization header
- Invalid JWT token
- Expired JWT token

### 403 Forbidden Responses
- User ID in path doesn't match authenticated user
- User ID in request body doesn't match authenticated user
- Attempting to access another user's resources

## Testing Authentication

### Valid Request
```bash
curl -X GET \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  http://localhost:8000/signup/users/user123/tasks
```

### Invalid Token Request
```bash
curl -X GET \
  -H "Authorization: Bearer invalid.token.here" \
  http://localhost:8000/signup/users/user123/tasks
# Response: 401 Unauthorized
```

### Mismatched User Request
```bash
curl -X GET \
  -H "Authorization: Bearer valid_jwt_for_user456" \
  http://localhost:8000/signup/users/user123/tasks
# Response: 403 Forbidden
```

## Security Best Practices

1. **Always use HTTPS in production**
2. **Keep BETTER_AUTH_SECRET secure and never expose in client-side code**
3. **Validate JWT tokens on every request**
4. **Enforce user data isolation at the API and database levels**
5. **Use appropriate token expiration times**
6. **Implement proper error handling without exposing sensitive information**