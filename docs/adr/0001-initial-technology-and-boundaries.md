# ADR 0001: Initial Technology Direction and Service Boundaries

- Status: Accepted as initial baseline
- Date: 2026-10-30

## Context
The platform needs a responsive workspace, durable control plane, agent runtime, and separate execution environment for untrusted code.

## Decision
React/Vite/TypeScript/Tailwind/Monaco frontend; FastAPI/Python control plane; PostgreSQL persistence; Redis queue/cache; disposable hardened Docker-based workers; Git/GitHub adapters; S3-compatible artifacts.

API/control-plane services stay separate from untrusted code execution. PostgreSQL is durable source of truth.

## Consequences
Rapid iteration and clear boundaries, but Python worker orchestration needs concurrency/resource discipline; Docker alone is insufficient as hostile-code isolation; Redis is not durable truth; provider/deployment details require later ADRs.

## Revisit when
Isolation guarantees are insufficient, measured scale justifies another queue/runtime, or enterprise deployment imposes new constraints.
