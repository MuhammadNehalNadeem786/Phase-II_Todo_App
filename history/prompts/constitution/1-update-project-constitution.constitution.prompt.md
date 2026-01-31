---
id: 1
title: "update-project-constitution"
stage: "constitution"
date_iso: "2026-01-16"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "1-todo-web-app"
user: "user"
command: "/sp.constitution"
labels: ["constitution", "setup", "governance"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - .specify/memory/constitution.md
tests_yaml: |
  - none
prompt_text: "# Full Stack Todo Web Application Constitution\n\n## Core Principles\n\n### Specification as Source of Truth\nAll system behavior must be defined in specs before implementation. Specs override assumptions, opinions, and ad-hoc decisions.\n\n### Contract-Driven Full-Stack Development\nFrontend, backend, and database interactions must follow explicit contracts. No implicit behavior is allowed across system boundaries.\n\n### User Isolation & Security First\nEach authenticated user may access and modify only their own tasks. Authorization is enforced on every request without exception.\n\n### Predictability Over Complexity\nSimple, explicit, and testable behavior is preferred over clever abstractions. Stability and correctness take priority over feature quantity.\n\n### Hackathon Execution Discipline\nThe system must remain demo-ready throughout development. Core functionality must be complete and reliable.\n\n### Behavior Specification Compliance\nIf behavior is not specified, it does not exist. All contributors, tools, and AI systems (including Claude Code) must comply with this constitution.\n\n## Key Standards\nIncludes Spec-Driven Standards, API Standards, Authentication & Authorization Standards, Data & Persistence Standards\n\n### Spec-Driven Standards\n- All features must map to one of the defined specs (Spec-1, Spec-2, Spec-3).\n- No code may be written without an associated spec definition.\n- Changes to behavior require spec updates before code changes.\n\n### API Standards\n- RESTful design with explicit HTTP methods:\n  - GET, POST, PUT, DELETE, PATCH\n- Consistent request and response formats.\n- Predictable error handling using standard HTTP status codes.\n\n### Authentication & Authorization Standards\n- Authentication is handled on the frontend using Better Auth.\n- Authorization is enforced on the backend using JWT verification.\n- All protected API endpoints require a valid JWT token.\n- User identity is extracted exclusively from verified JWTs.\n\n### Data & Persistence Standards\n- All task data is stored in Neon Serverless PostgreSQL.\n- SQLModel is used as the ORM layer.\n- All database queries must be filtered by authenticated user ID.\n- Task ownership is enforced at the data-access level.\n\n## Constraints\nTechnology Constraints, Security Constraints, Behavioral Constraints\n\n### Technology Constraints\n- **Frontend:** Next.js 16+ (App Router)\n- **Backend:** Python FastAPI\n- **ORM:** SQLModel\n- **Database:** Neon Serverless PostgreSQL\n- **Spec-Driven Tooling:** Claude Code + Spec-Kit Plus\n- **Authentication:** Better Auth with JWT\n\nNo alternative frameworks or stacks are permitted during the hackathon.\n\n### Security Constraints\n- JWT tokens must be included in every API request using:\n  - `Authorization: Bearer <token>`\n- JWTs must be verified using a shared secret:\n  - `BETTER_AUTH_SECRET`\n- Requests without valid tokens must return `401 Unauthorized`.\n- User ID in the request path must match the authenticated JWT user ID.\n- Cross-user data access is strictly forbidden.\n\n### Behavioral Constraints\n- Undocumented behavior is not allowed.\n- Backend must never trust client-provided user identity.\n- All task operations must enforce ownership checks.\n\n## Governance\nSuccess Criteria and Non-Negotiable Rule\n\nThe project is considered successful if:\n- All five basic Todo features are implemented as a web application.\n- RESTful API endpoints function as defined and are fully secured.\n- Users can sign up and sign in using Better Auth.\n- JWT-based authorization is enforced on every API request.\n- Each user can only see and manage their own tasks.\n- Data persists reliably in Neon Serverless PostgreSQL.\n- Frontend and backend behavior strictly match the specs.\n- No undocumented or unsafe behavior exists.\n- The application is stable and demo-ready.\n\n> **If behavior is not specified, it does not exist.**\nAll contributors, tools, and AI systems (including Claude Code) must comply with this constitution.\n"
response_text: "Updated the project constitution file at .specify/memory/constitution.md with the full stack todo web application constitution. The constitution defines core principles, standards, constraints, and governance rules for the project. It emphasizes specification-driven development, security-first approach with user isolation, and technology constraints using Next.js, FastAPI, SQLModel, and Neon PostgreSQL with Better Auth for authentication. The version has been set to 1.0.0 with ratification and last amended dates as 2026-01-16."
outcome: "Successfully created and updated the project constitution file with comprehensive governance rules for the full stack todo web application project."
evaluation: "The constitution file has been properly created with all required sections and follows the specified format with appropriate versioning and dates."
---

# PHR: update-project-constitution

## Summary
Updated the project constitution file at `.specify/memory/constitution.md` with the full stack todo web application constitution. The constitution defines core principles, standards, constraints, and governance rules for the project. It emphasizes specification-driven development, security-first approach with user isolation, and technology constraints using Next.js, FastAPI, SQLModel, and Neon PostgreSQL with Better Auth for authentication. The version has been set to 1.0.0 with ratification and last amended dates as 2026-01-16.

## Details
- Created a comprehensive constitution document with core principles
- Defined technology stack constraints and security requirements
- Established governance rules and success criteria
- Applied proper versioning and date formatting
- Included a sync impact report at the top of the file

## Files Modified
- `.specify/memory/constitution.md`: Main constitution file with all governance rules

## Outcome
Successfully created and updated the project constitution file with comprehensive governance rules for the full stack todo web application project.