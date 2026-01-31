# Data Model: Frontend Application & Full-Stack Integration (Next.js)

## Frontend State Models

### User Session Entity
```
UserSession {
  userId: string
  token: string
  email: string
  isAuthenticated: boolean
  expiresAt: Date
}
```

**Fields**:
- `userId`: Unique identifier for the authenticated user
- `token`: JWT token for API authentication
- `email`: User's email address
- `isAuthenticated`: Boolean indicating authentication status
- `expiresAt`: Expiration timestamp for token validity

**State Transitions**:
- Unauthenticated → Authenticating (login/signup initiated)
- Authenticating → Authenticated (successful login/signup)
- Authenticated → Unauthenticated (logout/expired token)

### Task Entity (Frontend Representation)
```
Task {
  id: number
  title: string
  description: string
  completed: boolean
  userId: string
  createdAt: Date
  updatedAt: Date
}
```

**Fields**:
- `id`: Unique identifier for the task
- `title`: Task title (required, 1-255 characters)
- `description`: Optional task description (max 1000 characters)
- `completed`: Boolean indicating completion status
- `userId`: Owner of the task (matches authenticated user)
- `createdAt`: Creation timestamp
- `updatedAt`: Last modification timestamp

### API Response Models

#### Success Response
```json
{
  "success": true,
  "data": {},
  "message": "optional message"
}
```

#### Error Response
```json
{
  "success": false,
  "error": {
    "code": "error_code",
    "message": "human-readable message",
    "details": {}
  }
}
```

## Component State Models

### Form State
```
FormState {
  values: Object
  errors: Object
  touched: Object
  isSubmitting: boolean
  isValid: boolean
}
```

### Loading State
```
LoadingState {
  isLoading: boolean
  loadingMessage: string
  progress: number
}
```

### Error State
```
ErrorState {
  hasError: boolean
  errorMessage: string
  errorType: "validation" | "network" | "server" | "auth"
  canRetry: boolean
}
```

## API Contract Models

### Authentication Requests/Responses

#### Login Request
```json
{
  "email": "user@example.com",
  "password": "secure_password"
}
```

#### Login Response
```json
{
  "user": {
    "id": "user123",
    "email": "user@example.com"
  },
  "token": "jwt_token_string"
}
```

#### Signup Request
```json
{
  "email": "user@example.com",
  "password": "secure_password",
  "confirmPassword": "secure_password"
}
```

### Task Operation Models

#### Create Task Request
```json
{
  "title": "New task title",
  "description": "Task description",
  "completed": false,
  "user_id": "authenticated_user_id"
}
```

#### Task Response
```json
{
  "id": 123,
  "title": "Task title",
  "description": "Task description",
  "completed": false,
  "user_id": "user123",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```

#### Update Task Request
```json
{
  "title": "Updated title",
  "description": "Updated description",
  "completed": true
}
```

## Validation Rules

### Form Validation
- Email: Must be valid email format
- Password: Minimum 8 characters with complexity requirements
- Task Title: 1-255 characters
- Task Description: Max 1000 characters

### Authentication Validation
- Token must be present and valid for protected routes
- Token expiration must be checked before API requests
- User ID in JWT must match expected user context

### Task Validation
- Users can only modify tasks belonging to their user ID
- Task ownership is validated on both frontend and backend
- Completed status can only be toggled by task owner

## UI State Flows

### Authentication Flow States
```
LoginPage/signupPage
    ↓ (submit credentials)
Authenticating
    ↓ (success)           ↓ (failure)
DashboardPage ← ErrorPage
```

### Task Management Flow States
```
DashboardPage (shows task list)
    ↓ (click create)
TaskFormPage
    ↓ (submit)        ↓ (cancel)
DashboardPage ← DashboardPage
    ↓ (click task)
TaskDetailPage
    ↓ (edit/delete)
DashboardPage
```

## Error Handling States

### Network Error Recovery
- Show user-friendly error messages
- Provide retry options where appropriate
- Cache optimistic updates for retry
- Gracefully degrade functionality when offline