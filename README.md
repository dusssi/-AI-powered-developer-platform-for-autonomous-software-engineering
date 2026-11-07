# BuckLabs Dev

AI-powered developer platform for autonomous software engineering.

BuckLabs Dev is a human-governed engineering workspace: developers connect authorized repositories, delegate bounded work to replaceable coding engines, review plans and diffs, and verify results before delivery.

## Current state

This repository is an early development foundation. It currently contains a FastAPI control-plane API with baseline authentication, owner-scoped workspaces, and GitHub repository URL registration (metadata only), plus architecture, security, migration, test, and CI foundations.

**It is not yet a working autonomous coding platform.** Repository cloning/indexing, task orchestration, engine adapters, approvals, isolated workers, frontend, diff review, and GitHub PR delivery remain roadmap work.

## Architecture

- **Platform control plane:** owns identity, tenancy, workspace authorization, task state, approval policy, and audit history.
- **Engine adapters:** OpenCode, Codex, Gemini CLI, Aider, and potentially OpenHands are replaceable coding engines behind one platform-owned contract.
- **Tool gateway:** validates and authorizes every side effect. Engine/model permission claims are never trusted.
- **Isolated workers:** run repository commands in disposable task-scoped environments, never in the API process.
- **Verifier:** independently runs configured tests/builds and records exact results before a task can be marked complete.

See [System Architecture](docs/architecture/SYSTEM_ARCHITECTURE.md), [Security Model](docs/security/SECURITY_MODEL.md), and [Agent Engine Integration](docs/architecture/AGENT_ENGINE_INTEGRATION.md).

## Backend quickstart

See [backend/README.md](backend/README.md). Requires Python 3.11+.

## Repository principles

- Human control over writes, execution, and delivery.
- No unrestricted host access or platform secrets in coding workers.
- Deny overrides allow; approvals are scoped, expiring, and auditable.
- No success claims without independent verification evidence.
- Upstream engines remain pinned, replaceable integrations; no blind vendor-code copying.

## Roadmap

See [docs/roadmap/ROADMAP.md](docs/roadmap/ROADMAP.md).