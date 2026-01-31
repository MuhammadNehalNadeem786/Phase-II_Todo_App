<!-- SYNC IMPACT REPORT
Version change: N/A -> 1.0.0
Modified principles: None (new constitution)
Added sections: All sections
Removed sections: None
Templates requiring updates:
  - .specify/templates/plan-template.md ✅ updated
  - .specify/templates/spec-template.md ✅ updated
  - .specify/templates/tasks-template.md ✅ updated
  - .specify/templates/commands/*.md ⚠ pending
  - README.md ⚠ pending
Follow-up TODOs: None
-->

# Full Stack Todo Web Application Constitution

## Core Principles

### Specification as Source of Truth
All system behavior must be defined in specs before implementation. Specs override assumptions, opinions, and ad-hoc decisions.

### Contract-Driven Full-Stack Development
Frontend, backend, and database interactions must follow explicit contracts. No implicit behavior is allowed across system boundaries.

### User Isolation & Security First
Each authenticated user may access and modify only their own tasks. Authorization is enforced on every request without exception.

### Predictability Over Complexity
Simple, explicit, and testable behavior is preferred over clever abstractions. Stability and correctness take priority over feature quantity.

### Hackathon Execution Discipline
The system must remain demo-ready throughout development. Core functionality must be complete and reliable.

### Behavior Specification Compliance
If behavior is not specified, it does not exist. All contributors, tools, and AI systems (including Claude Code) must comply with this constitution.

## Key Standards
Includes Spec-Driven Standards, API Standards, Authentication & Authorization Standards, Data & Persistence Standards

### Spec-Driven Standards
- All features must map to one of the defined specs (Spec-1, Spec-2, Spec-3).
- No code may be written without an associated spec definition.
- Changes to behavior require spec updates before code changes.

### API Standards
- RESTful design with explicit HTTP methods:
  - GET, POST, PUT, DELETE, PATCH
- Consistent request and response formats.
- Predictable error handling using standard HTTP status codes.

### Authentication & Authorization Standards
- Authentication is handled on the frontend using Better Auth.
- Authorization is enforced on the backend using JWT verification.
- All protected API endpoints require a valid JWT token.
- User identity is extracted exclusively from verified JWTs.

### Data & Persistence Standards
- All task data is stored in Neon Serverless PostgreSQL.
- SQLModel is used as the ORM layer.
- All database queries must be filtered by authenticated user ID.
- Task ownership is enforced at the data-access level.

## Constraints
Technology Constraints, Security Constraints, Behavioral Constraints

### Technology Constraints
- **Frontend:** Next.js 16+ (App Router)
- **Backend:** Python FastAPI
- **ORM:** SQLModel
- **Database:** Neon Serverless PostgreSQL
- **Spec-Driven Tooling:** Claude Code + Spec-Kit Plus
- **Authentication:** Better Auth with JWT

No alternative frameworks or stacks are permitted during the hackathon.

### Security Constraints
- JWT tokens must be included in every API request using:
  - `Authorization: Bearer <token>`
- JWTs must be verified using a shared secret:
  - `BETTER_AUTH_SECRET`
- Requests without valid tokens must return `401 Unauthorized`.
- User ID in the request path must match the authenticated JWT user ID.
- Cross-user data access is strictly forbidden.

### Behavioral Constraints
- Undocumented behavior is not allowed.
- Backend must never trust client-provided user identity.
- All task operations must enforce ownership checks.

## Governance
Success Criteria and Non-Negotiable Rule

The project is considered successful if:
- All five basic Todo features are implemented as a web application.
- RESTful API endpoints function as defined and are fully secured.
- Users can sign up and sign in using Better Auth.
- JWT-based authorization is enforced on every API request.
- Each user can only see and manage their own tasks.
- Data persists reliably in Neon Serverless PostgreSQL.
- Frontend and backend behavior strictly match the specs.
- No undocumented or unsafe behavior exists.
- The application is stable and demo-ready.

> **If behavior is not specified, it does not exist.**
All contributors, tools, and AI systems (including Claude Code) must comply with this constitution.

**Version**: 1.0.0 | **Ratified**: 2026-01-16 | **Last Amended**: 2026-01-16