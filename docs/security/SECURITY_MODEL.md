# Security Model and Threat Baseline

## Objective
Enable AI-assisted development without granting ambient authority over the host, unrelated repositories, credentials, or other tenants.

## Untrusted inputs
Prompts, uploads, repository content, comments, issue descriptions, build scripts, tests, generated code, model/tool output, third-party MCP servers, and downloaded dependencies.

## Permission modes
- `read_only`: inspect authorized workspace; no mutation or process execution.
- `workspace_write`: modify authorized workspace; execution still requires worker policy.
- `elevated_action`: narrowly scoped, time-bound approval for a specific sensitive operation.

No unrestricted mode is the default. Deny overrides allow. Authorization is server-side on every operation. Approval is scoped to action, workspace, and time, and cannot be replayed for another command/resource. Models cannot grant permissions.

## Filesystem
Canonicalize paths, reject traversal and symlink escapes, re-check at execution time, mount only task workspace, keep host home/sockets/config/secrets outside workers, use read-only mounts where possible, enforce boundaries at OS layer.

## Worker isolation
Disposable, least-privileged, non-root workers; read-only base filesystem where practical; scoped workspace mount; CPU/memory/process/disk/time quotas; no privileged mode, host Docker socket, host PID or shared host network; drop capabilities; use seccomp/MAC where supported; destroy after task. Docker alone is not a complete hostile-code sandbox.

## Network
Worker egress denied by default. Permit only policy-approved destinations through controlled proxy. Block cloud metadata and internal control-plane services.

## Secrets and tenancy
Never expose platform credentials to untrusted workers. Use short-lived scoped tokens, redact logs/model context, use a secret manager, never commit .env. Scope database/object/cache access by tenant/workspace. Do not share active workers across tenants. Cross-tenant tests are mandatory.

## Audit
Record actor, tenant, workspace, task, tool, policy decision, approval ref, worker identity, timestamps, outcome, artifact refs. Never log secret values.

## Required security tests
Path traversal/symlink escape; unauthorized workspace access; deny-overrides-allow; approval replay/scope mismatch; time/resource exhaustion; worker egress; secret leakage; cross-tenant DB/cache/artifact access; cancellation races and duplicate task delivery.
