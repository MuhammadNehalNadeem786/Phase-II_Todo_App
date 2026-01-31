# Backend Skill

**Name:** `backend-skill`  
**Description:** Master backend development by generating API routes, handling requests/responses, and implementing validation, middleware, and testing.

---

## Instructions

### 1. Project Initialization
- Initialize a backend project using **Express.js**, **FastAPI**, or **Flask**.
- Organize your project structure with folders:
  - `routes` – for API route definitions
  - `controllers` – for request handling logic
  - `services` – for business logic
- Install necessary dependencies:
  - **Routing:** `express` / `fastapi` / `flask`
  - **Validation:** `joi` / `pydantic` / `marshmallow`
  - **Testing:** `jest` / `pytest`

---

### 2. Route Generation
- Create RESTful API routes for CRUD operations:
  - **Create:** `POST /resource`
  - **Read:** `GET /resource` or `GET /resource/:id`
  - **Update:** `PUT/PATCH /resource/:id`
  - **Delete:** `DELETE /resource/:id`
- Support route parameters, query strings, and request body parsing.

---

### 3. Request & Response Handling
- Validate incoming requests using a validation library.
- Parse JSON request bodies and query parameters.
- Send structured JSON responses with consistent HTTP status codes.
- Implement centralized error handling for validation and server errors.

---

### 4. Middleware & Utilities
- Implement middleware for:
  - Logging requests
  - Authentication and authorization
  - Error handling
- Ensure proper integration of validation and authentication flows.

---

### 5. Testing
- Write **unit tests** for controllers and services.
- Write **integration tests** for API routes.
- Test both success and failure scenarios to ensure robustness.

---

## Example Tasks

- Build a `/users` API with `GET` and `POST` endpoints.
- Validate request data when creating a user.
- Implement business logic in services for handling user data.
- Return structured JSON responses:

```json
{
  "status": "success",
  "data": [
    { "id": 1, "name": "John Doe", "email": "john@example.com" }
  ]
}
