# System Architecture

## Components

**Web workspace:** React, Vite, TypeScript, Tailwind, Monaco. Workspace navigation, editor, agent conversation, task timeline, diff viewer, terminal output, approvals.

**API/control plane:** FastAPI for authenticated APIs, workspace operations, task creation, policy decisions, and WebSocket/SSE streaming. It must not execute untrusted repository code in the API process.

**Agent runtime:** task state, planning, model interaction, tool selection, validation, cancellation, retries, result synthesis.

**Tool gateway:** server-side typed registry. Each call passes authentication, workspace authorization, schema and semantic validation, policy evaluation, approval, execution, output budgeting, and audit recording.

**Execution workers:** disposable isolated workers execute repository commands/tests with only task-scoped inputs and no platform secrets.

**Data services:** PostgreSQL is authoritative for users, workspaces, tasks, policies, approvals, audit metadata. Redis supports queues/short-lived coordination/cache. Object storage holds repository snapshots and task artifacts.

## Logical flow

```text
Browser -> FastAPI Control Plane -> PostgreSQL
                 |
                 +-> Redis Queue -> Agent Runtime -> Model Gateway
                                         |
                                         v
                                    Tool Gateway
                                         |
                                Policy / Approvals
                                         |
                                         v
                                  Isolated Worker
                                         |
                                 Verifier + Audit
                                         |
                                  Browser task stream
```

## Trust boundaries
Browser/API; API/runtime; runtime/model provider; runtime/tool gateway; tool gateway/worker; worker/repository content; worker/network; tenant/tenant.

## Agent states
queued, initializing, planning, awaiting_approval, executing, verifying, completed, failed, cancelled. Persist transitions; terminal states cannot silently return to execution; retries create traceable attempts.

## Tool pipeline
Resolve allowlisted tool; cancellation/deadline; JSON schema validation; semantic/workspace validation; policy decision; approval; isolated execution; time/output/resource budgets; error classification; audit record and typed result.

## Concurrency and resilience
Parallelize independent read-only operations. Serialize conflicting writes or use explicit locking/versioning. Persist task state in PostgreSQL. Treat queue delivery as at-least-once unless proven otherwise. Define idempotency. Worker loss is a failed attempt, never false success. Client disconnects do not erase task state.
