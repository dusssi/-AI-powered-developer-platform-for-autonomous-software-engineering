# Agent Engine Integration Architecture

Status: proposed integration contract for BuckLabs Dev.

## Decision

BuckLabs Dev owns the platform control plane: identity, tenancy, workspace authorization, task state, approvals, audit events, and execution policy. Coding engines are replaceable execution adapters. No upstream engine owns platform authorization or task truth.

The initial engine strategy is **adapter-first**, not a monorepo graft of upstream code. Prefer stable external interfaces (CLI subprocess with structured I/O, HTTP service API, or MCP where suitable). Do not import internal modules from upstream forks as application dependencies.

## Repositories reviewed

| Local fork | Product role | Reusable concepts | Integration posture |
|---|---|---|---|
| `dusssi/opencode` | Coding agent + provider/tool runtime | Model/provider routing, typed tool abstractions, tool-call streaming, session/context handling | Adapter candidate; pin a release/commit and use supported CLI/server interface |
| `dusssi/codex` | Terminal coding agent/runtime | Explicit turn/session lifecycle, approval requests, sandbox/network policy, event protocol, agent graph | Adapter candidate; inspect app-server protocol and exec-server boundary before wiring |
| `dusssi/gemini-cli` | Terminal agent | Typed tool registry, confirmation events, hooks, context compression, loop detection, sandbox manager | Adapter candidate; use CLI/headless mode and normalize events |
| `dusssi/aider` | Git-aware pair programmer | Repo map, edit formats, git integration, lint/test feedback, model abstraction | Adapter candidate for patch-oriented coding; keep its git operations inside workspace |
| `dusssi/OpenHands` | Software engineering agent/runtime | Workspace/conversation abstractions, event-stream runtime, agent-server separation, runtime providers | Potential isolated worker backend; do not run in API process |
| `dusssi/agent-desktop` | Computer-use interface | Observable desktop sessions, action APIs, explicit application/window commands | Separate optional capability; not part of first coding MVP |
| `dusssi/claude-code-from-source-bucky` | Architecture research notes | Agent loop, tool boundary, sub-agent lifecycle, context and permission observations | Research reference only; not an executable dependency |
| `dusssi/claw-code-bucky` | Python/Rust harness experiments | Session persistence, permission-denial structures, command/tool inventory, runtime decomposition | Prototype/reference; reuse only after independent tests and production hardening |
| `dusssi/awesome-prompts` | Prompt/framework catalog | Plan-first coding, context engineering, eval, reliability, safety and tool-schema patterns | Curated prompt/evaluation source; never treat prompt text as an authorization mechanism |

## Platform-owned contracts

### Engine adapter

Each adapter must implement these conceptual operations:

- `capabilities()`: return engine name/version, supported models, tools, streaming, cancellation, and structured-output support.
- `start(task_context)`: start one task attempt with a scoped workspace snapshot and task policy.
- `send(input)`: submit task/user input using a documented protocol.
- `events()`: stream normalized typed events (message, plan, tool request, approval request, tool result, file change, usage, warning, error, terminal result).
- `cancel(reason)`: request cooperative cancellation, then let the worker supervisor enforce a hard deadline.
- `close()`: release the process/session and all task-scoped resources.

The platform normalizes adapter-specific events into its own event schema. Raw provider/engine payloads are retained only where useful and safe, with size limits and secret redaction.

### Task state machine

Persist transitions in PostgreSQL:

`queued -> initializing -> planning -> awaiting_approval -> executing -> verifying -> completed`

Failure/cancellation are explicit terminal outcomes: `failed`, `cancelled`. A task may move from `planning` or `executing` to `awaiting_approval` and back only through a recorded, scoped approval decision. Retries create a new attempt linked to the parent task; they do not erase prior history.

### Tool gateway

All side effects go through the BuckLabs tool gateway, regardless of engine:

1. Authenticate actor and resolve tenant/workspace/task scope.
2. Validate tool name, JSON schema, paths, arguments and resource limits.
3. Apply server-side policy (deny overrides allow).
4. Require specific, expiring approval for sensitive actions.
5. Dispatch to a task-scoped isolated worker.
6. Enforce time, CPU, memory, process, output and filesystem quotas.
7. Record request, policy decision, approval, execution result and artifact references.
8. Return a typed result to the engine adapter.

A model or engine cannot grant itself permissions. UI controls are not security boundaries.

## Initial adapter order

1. **OpenCode adapter** — validate headless/server protocol, event streaming, provider configuration and tool delegation. It is a good broad agent candidate, but must not bypass the platform tool gateway.
2. **Codex adapter** — validate app-server JSON-RPC/event schemas, approval protocol, cancellation and sandbox interface. Strong candidate for a first high-assurance coding runtime.
3. **Gemini CLI adapter** — evaluate non-interactive mode, session IDs, structured tool events, hooks, confirmation prompts and output normalization.
4. **Aider adapter** — add a patch-oriented engine profile with repository map and lint/test feedback.
5. **OpenHands runtime adapter** — evaluate as a separately deployed worker service only after worker isolation, egress and tenant boundaries have passed security review.
6. **Desktop adapter** — separate product milestone with explicit user opt-in and device-side authorization.

Do not enable arbitrary user-configured commands, arbitrary MCP servers, desktop controls, or unrestricted network access in the first release.

## Security invariants

- The API/control plane never executes repository code.
- Workers are disposable, least-privileged, task-scoped, and isolated from platform secrets.
- Network egress is denied by default and controlled by policy.
- Filesystem operations are canonicalized and revalidated at execution time; symlink/path traversal escapes are blocked.
- Concurrent write-capable agents do not share a mutable working tree. Use isolated worktrees/snapshots and explicit merge conflict handling.
- Every engine event/tool request is correlated to actor, tenant, workspace, task, attempt and worker.
- Cancellation, retries, timeouts and worker loss are visible and auditable.
- No task is marked successful without verifier evidence. A successful model response is not proof that tests passed.
- Upstream forks remain independently versioned; record source commit, license, provenance and patch set before any code vendoring.

## Integration readiness gates per engine

- [ ] License and NOTICE obligations reviewed.
- [ ] Exact upstream commit and release pinned.
- [ ] CLI/server protocol tested with fixtures.
- [ ] No direct database writes or authorization bypass.
- [ ] Tool calls normalized into the platform tool gateway.
- [ ] Read-only mode verified.
- [ ] Write actions confined to a disposable task workspace.
- [ ] Approval round-trip tested, including rejection and expiry.
- [ ] Streaming, reconnect, cancellation and process cleanup tested.
- [ ] Time/output/resource budgets enforced outside the model.
- [ ] Secret redaction and prompt-injection test suite passed.
- [ ] Test/build result comes from an independent verifier.
- [ ] Engine crash, malformed event and duplicate-delivery behavior tested.

## First implementation slice

Before wiring an engine, establish the platform-owned interfaces and tests:

- Pydantic schemas for task, attempt, event, approval and adapter capability.
- An adapter protocol and a deterministic fake adapter for tests.
- A persisted task state machine with validated transitions.
- Event normalization and correlation IDs.
- A no-op/read-only adapter smoke test.
- Security tests for unauthorized workspace access, approval scope/replay, path traversal, cancellation and terminal-state integrity.

This gives every engine one stable contract and keeps the security model consistent.
