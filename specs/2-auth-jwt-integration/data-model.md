# Data Model: Authentication & Security Integration (Better Auth + JWT)

## JWT Token Structure

### User Identity Claims
```json
{
  "userId": "string",
  "user_id": "string",
  "email": "string",
  "iat": "number (timestamp)",
  "exp": "number (timestamp)"
}
```

**Fields**:
- `userId` or `user_id`: Unique identifier for the authenticated user
- `email`: User's email address (optional depending on Better Auth config)
- `iat`: Issued at timestamp
- `exp`: Expiration timestamp

## API Request Flow

### Authenticated Request Structure
```
POST /signup/users/{user_id}/tasks
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "title": "Task title",
  "description": "Task description",
  "completed": false,
  "user_id": "{authenticated_user_id}"
}
```

### Token Verification Process
1. Extract JWT from `Authorization` header
2. Verify token signature using `BETTER_AUTH_SECRET`
3. Validate token expiration
4. Decode user identity from payload
5. Compare authenticated user ID with requested user ID
6. Proceed with business logic or return 401/403

## Error Response Models

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

## Entity Relationships

### User-Task Relationship
```
User (1) <---> (Many) Task
- Each user has many tasks
- Each task belongs to exactly one user
- User ID is validated at both JWT level and request path level
```

## Validation Rules

### Authentication Validation
- JWT must be present in `Authorization` header
- JWT signature must be valid
- JWT must not be expired
- User ID in JWT must match user ID in request path

### Authorization Validation
- Authenticated user can only access their own tasks
- Cross-user access attempts return 403 Forbidden
- Request body user_id must match authenticated user_id