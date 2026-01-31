---
id: 7
title: frontend-nextjs-integration-plan
stage: plan
date: 2026-01-24
surface: agent
model: Claude Sonnet 4.5
feature: 3-frontend-nextjs-integration
branch: 3-frontend-nextjs-integration
user: claude
command: /sp.plan
labels: [frontend, nextjs, authentication, integration]
links:
  spec: ../specs/3-frontend-nextjs-integration/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/3-frontend-nextjs-integration/plan.md
 - specs/3-frontend-nextjs-integration/research.md
 - specs/3-frontend-nextjs-integration/data-model.md
 - specs/3-frontend-nextjs-integration/quickstart.md
 - specs/3-frontend-nextjs-integration/contracts/api-contracts.md
 - .specify/memory/agents/claude.md
tests:
 - tests/frontend/
---

## Prompt

Project: Full Stack Todo Web Application
Spec-3: Frontend Application & Full-Stack Integration (Next.js)

## Implementation Approach
- Follow a spec-first, implementation-second workflow
- Frontend strictly consumes backend API (Spec-1 + Spec-2)
- Ensure all behavior adheres to `/sp.specify` success criteria
- Maintain separation between UI components, API client, and authentication handling

## Architecture Sketch
- Next.js 16+ with App Router for routing and page management
- Responsive UI components for task list, task forms, buttons, and modals
- Frontend API client managing all communication with backend endpoints
- JWT automatically attached to API requests
- Auth-aware routing and UI state management
- Error and loading state handling integrated throughout the UI

## Phase Breakdown

### Phase 1: Project Setup
- Initialize Next.js project with App Router
- Configure project structure (pages, components, hooks, API client)
- Install necessary dependencies (Better Auth, Axios/Fetch, Tailwind or CSS modules)

### Phase 2: UI Development
- Build responsive UI for task list and task forms
- Implement task CRUD lifecycle in the frontend:
  - Create tasks
  - Update tasks
  - Delete tasks
  - Toggle completion
- Ensure UI updates reflect backend state
- Implement loading and empty states

### Phase 3: API Integration
- Implement frontend API client with JWT token support
- Attach JWT token to all requests via `Authorization: Bearer <token>` header
- Handle 401 Unauthorized and 403 Forbidden responses gracefully
- Integrate API endpoints for user-specific tasks

### Phase 4: Full-Stack Testing
- Perform end-to-end testing of login → task management → logout
- Validate that UI behavior aligns with backend responses
- Test error handling, empty states, and edge cases
- Confirm auth-aware routing works as expected

## Decisions Needing Documentation
- Choice of Next.js 16+ App Router over older pages router
- State management approach (React hooks vs Redux/Context)
- UI framework or styling method (Tailwind, CSS modules)
- API client choice (Axios vs Fetch)
- Error handling approach for 401/403 and network errors

## Testing Strategy
- End-to-end tests for login, task CRUD, and logout flows
- Manual and automated UI validation
- Verify JWT header injection on all API requests
- Confirm that unauthorized requests redirect or display errors correctly
- Validate responsive design on desktop and mobile devices

## Quality Validation
- UI fully implements task lifecycle as specified
- Auth-protected routes enforce frontend restrictions
- Frontend strictly follows Spec-Driven API contracts
- Loading, empty, and error states handled consistently
- End-to-end behavior verified for all user actions

## Response snapshot

I've completed the implementation planning for the Frontend Application & Full-Stack Integration feature. The following artifacts were created:

1. **plan.md**: Complete implementation plan with technical context, constitution check, and project structure
2. **research.md**: Technology selection research with rationale for Next.js, React hooks, Tailwind CSS, Axios, and Better Auth
3. **data-model.md**: Frontend state models, component state models, API response models, and validation rules
4. **contracts/api-contracts.md**: Complete API contracts for authentication and task management endpoints
5. **quickstart.md**: Step-by-step setup guide for the Next.js frontend application
6. **Updated agent context**: Updated the agent context file with frontend technologies and patterns

The plan covers all aspects of the frontend development including:
- Next.js 16+ with App Router implementation
- Authentication integration with Better Auth
- API client with JWT token handling
- Responsive UI component architecture
- Error handling and loading states
- Full-stack integration with the existing backend API

The implementation follows the spec-driven development approach and maintains consistency with the existing backend architecture from Spec-1 and Spec-2.

## Outcome

- ✅ Impact: Complete frontend implementation plan ready for development
- 🧪 Tests: API contracts defined for comprehensive testing
- 📁 Files: 6 planning artifacts created with updated agent context
- 🔁 Next prompts: Ready for task breakdown with /sp.tasks
- 🧠 Reflection: Comprehensive frontend architecture aligned with backend APIs

## Evaluation notes (flywheel)

- Failure modes observed: None - plan aligns with existing architecture
- Graders run and results (PASS/FAIL): PASS - All constitution checks verified
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin task breakdown and implementation