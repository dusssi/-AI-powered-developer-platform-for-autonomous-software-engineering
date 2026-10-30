# Implementation Boundaries

## Current backend slice
The first API slice is intentionally limited to application setup, typed settings, process liveness, and process readiness. It does not implement user identity, workspace persistence, Git operations, agent execution, shell access, or sandboxing.

## Next safe increments
1. Add PostgreSQL-backed identity and workspace persistence.
2. Add authentication and authorization before exposing workspace data operations.
3. Add repository import through a Git provider adapter with narrowly scoped credentials.
4. Add task/run persistence and an event model.
5. Add the tool gateway and permission policy before any execution tools.
6. Add isolated workers only after an explicit threat-model review and isolation test suite.

## Readiness semantics
- `/health`: process is responsive.
- `/ready`: API configuration is loaded.
- Future infrastructure-aware readiness checks must independently verify dependencies and report degraded/unavailable states accurately.
