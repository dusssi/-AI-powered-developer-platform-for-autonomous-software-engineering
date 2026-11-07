# Roadmap

## Stage 0 — Foundation
- [x] Product direction and initial stack.
- [x] Architecture and trust boundaries.
- [x] Security baseline.
- [x] Engineering/contribution standards.
- [x] GitHub templates and repository hygiene.
- [ ] Confirm repository visibility and security settings.
- [ ] Select license and release policy.
- [ ] Create project board/milestones.

Exit criteria: docs reviewed, security invariants accepted, implementation boundaries stable.

## Stage 1 — Workspace foundation
- [x] Workspace persistence and CRUD APIs.
- [x] User registration/login baseline and owner-scoped workspace authorization.
- [x] Repository URL registration (metadata only).
- [ ] Add proper Git provider authorization and repository metadata fetch.
- [ ] Implement task-scoped repository snapshot/indexing service.
- [ ] Add frontend workspace/repository experience.

## Stage 2 — Platform-owned agent contracts
- [x] Add initial task context, normalized event, and adapter capability schemas (in-memory contract; persistence/approval schemas remain pending).
- [ ] Implement validated persisted task state machine.
- [x] Implement adapter protocol and deterministic fake adapter.
- [x] Define normalized event envelope and correlation IDs (durable event storage/stream transport remain pending).
- [ ] Add task history, cancellation, retry, and timeout semantics.

## Stage 3 — Safe execution
- [ ] Add policy engine with deny-overrides-allow semantics.
- [ ] Add scoped, expiring approval records and replay protection.
- [ ] Implement disposable isolated workers with no ambient platform secrets.
- [ ] Enforce filesystem confinement, resource quotas, and default-deny network egress.
- [ ] Add security regression suite for tenancy, path traversal, approvals, and worker escape boundaries.

## Stage 4 — First coding-engine integration
- [ ] Implement OpenCode adapter behind the platform adapter contract.
- [ ] Prove read-only mode and tool-gateway mediation.
- [ ] Add independent test/build verification and diff artifacts.
- [ ] Evaluate Codex adapter after the same contract and policy tests pass.
- [ ] Add Gemini CLI and Aider adapter profiles.

## Stage 5 — Verification and delivery
- [ ] File edit/diff review and artifact viewer.
- [ ] Test/build command profiles with bounded execution.
- [ ] Git branch/PR workflow with explicit human approval.
- [ ] Auditable task report with commands, exit codes, logs, and verification evidence.

## Stage 6 — Advanced runtimes
- [ ] Evaluate OpenHands as an isolated worker backend.
- [ ] Add isolated multi-agent decomposition and coordination.
- [ ] Add governed MCP integrations.
- [ ] Evaluate desktop/computer-use as a separate explicitly opted-in capability.

## Stage 7 — Managed cloud workflows
- [ ] Managed development environments.
- [ ] Deployment integrations with explicit approvals.
- [ ] Organization controls, policy management, and observability.
