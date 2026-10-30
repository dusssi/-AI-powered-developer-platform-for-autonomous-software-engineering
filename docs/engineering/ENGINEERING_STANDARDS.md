# Engineering Standards

## General
Typed service boundaries; business logic separated from framework glue; explicit state/errors; small focused modules; no swallowed exceptions or unsupported success claims.

## Backend
Python type hints; FastAPI; Pydantic contracts; Ruff; pytest; async I/O for network operations; bounded pools for blocking tasks. Never execute untrusted repo commands inside API process.

## Frontend
React + TypeScript strict mode; accessible reusable components; distinct server/local/task-event state. Frontend permission controls are UX only; server enforces authorization.

## APIs/events
Version contracts; stable task/event IDs; documented ordering; correlation IDs; explicit cancellation/retry semantics.

## Testing
Unit tests for policies/state/validation; integration tests for API/database/queue; worker isolation tests; critical journey E2E; security regression tests for every boundary failure.

## Documentation
Update docs with behavior changes; use ADRs for material decisions; include commands and expected outcomes in operational docs.
