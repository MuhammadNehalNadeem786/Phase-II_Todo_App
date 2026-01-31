# Agent Context: Frontend & Backend Integration (Next.js + FastAPI + JWT)

## Technologies Used
- Next.js 16+: React framework with App Router for frontend routing
- React: Component-based UI library
- Better Auth: Next.js authentication solution with JWT support
- Tailwind CSS: Utility-first CSS framework for styling
- Axios: HTTP client for API communication
- FastAPI: Modern Python web framework with automatic API documentation
- SQLModel: SQL databases with Python types using Pydantic and SQLAlchemy
- Neon Serverless PostgreSQL: Serverless PostgreSQL database service
- AsyncPG: Async PostgreSQL driver for Python
- Pydantic: Data validation and settings management using Python type hints
- python-jose: JWT token encoding/decoding and verification

## Architecture Components
- Next.js App Router for page routing and layout management
- RESTful API endpoints following standard HTTP methods
- Database session management with dependency injection
- User-based data isolation enforced at query level
- JWT-based authentication and authorization
- HTTPBearer security scheme for token extraction
- Centralized authentication dependencies in api.deps.auth
- Frontend API client with JWT token injection
- Protected route components for authentication enforcement
- Comprehensive error handling with standard HTTP status codes

## Key Implementation Patterns
- Next.js App Router: File-based routing with nested layouts
- React Hooks: State management and side effects in components
- SQLModel inheritance: Base classes for shared fields, table=True for database tables
- FastAPI dependencies: For database session management and authentication
- Async/await patterns: For non-blocking database operations
- Query-level filtering: All database queries must filter by user_id for security
- Pydantic validation: Automatic request/response validation
- HTTPBearer + Depends: Centralized JWT verification pattern
- Token payload extraction: User identity derived from JWT claims
- API Client Interceptors: Request/response handling with JWT attachment
- Component Composition: Reusable UI components with clear separation of concerns

## Security Considerations
- All API endpoints require JWT authentication
- User ID in URL path must match authenticated user from JWT
- Database queries must filter by user_id to prevent cross-user access
- Input validation through Pydantic models
- Proper error responses without sensitive information disclosure
- BETTER_AUTH_SECRET for JWT signing/verification
- Authorization enforced before business logic execution
- No client-provided user identity trusted - only JWT-derived identity
- Secure JWT token storage and transmission
- Frontend route protection with authentication checks
- API request interception to attach JWT tokens automatically

## Database Schema
- Tasks table with id, title, description, completed, user_id, created_at, updated_at
- Indexes on user_id for efficient user-based queries
- Foreign key relationship to users (conceptual - users handled separately)

## Frontend Component Structure
- App Router pages in src/app/: authentication routes, dashboard, task management
- Reusable components in src/components/: UI elements, auth forms, task cards
- Services in src/services/: API client, authentication, task operations
- Hooks in src/hooks/: Custom React hooks for state management
- Types in src/types/: TypeScript interfaces and type definitions

## API Contract Patterns
- Base URL: /signup/
- User-specific endpoints: /users/{user_id}/tasks/{task_id}
- Authorization header: "Authorization: Bearer <jwt_token>"
- Standard HTTP methods: GET, POST, PUT, DELETE, PATCH
- Consistent error response format
- JSON request/response bodies

## Authentication Flow
- Frontend authenticates user via Better Auth
- Better Auth issues signed JWT token
- Frontend sends JWT in Authorization header via API client interceptor
- Backend verifies JWT signature using BETTER_AUTH_SECRET
- Backend extracts user identity from JWT payload
- Backend enforces user-scoped access control
- Frontend enforces route protection based on authentication status

## Common Validation Rules
- Task title: Required, 1-255 characters
- Task description: Optional, max 1000 characters
- User ID: Must match authenticated user from JWT
- Completed: Boolean, default False
- JWT: Must be present, valid, and unexpired
- User ID in path: Must match authenticated user ID
- User ID in request body: Must match authenticated user ID
- Email: Valid email format for authentication
- Password: Minimum 8 characters with complexity requirements