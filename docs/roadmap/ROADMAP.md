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
Workspace model/API; authorized repository import; file browser/metadata; indexing/search; authentication and workspace authorization.

## Stage 2 — Agent runtime
Task state machine; model gateway; planner; tool registry/validation; streaming, cancellation, retries, audit events.

## Stage 3 — Safe execution
Permission/approval engine; worker lifecycle; filesystem confinement; process/resource quotas; network egress controls; security regression suite.

## Stage 4 — Editing and verification
Read/search/edit tools; diff review; test/build execution; result verification and task reports.

## Stage 5 — Integrations
GitHub branches/PRs; code review; governed MCP adapters.

## Stage 6 — Multi-agent and teams
Specialist agents; isolated worktrees/workspaces; team roles and shared policy.

## Stage 7 — Managed cloud workflows
Managed development environments; deployment integrations; organization controls and observability.
