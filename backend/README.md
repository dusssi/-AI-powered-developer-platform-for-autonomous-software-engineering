# BuckLabs Dev API

## Setup (PowerShell)
```powershell
cd backend
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e ".[dev]"
Copy-Item .env.example .env
```

For deployments set a unique strong `JWT_SECRET`, production database URL, `ENVIRONMENT=production`, and `EXPOSE_DOCS=false`. Store secrets in a secret manager, never Git.

## Database and run
```powershell
alembic upgrade head
uvicorn app.main:app --reload
```

- Liveness: http://127.0.0.1:8000/health
- API docs: http://127.0.0.1:8000/docs

## Implemented endpoints
- POST /api/v1/auth/register
- POST /api/v1/auth/login
- GET /api/v1/auth/me
- POST /api/v1/workspaces
- GET /api/v1/workspaces
- GET /api/v1/workspaces/{workspace_id}
- PATCH /api/v1/workspaces/{workspace_id}
- DELETE /api/v1/workspaces/{workspace_id}
- POST /api/v1/workspaces/{workspace_id}/repositories
- POST /api/v1/workspaces/{workspace_id}/tasks
- GET /api/v1/workspaces/{workspace_id}/tasks
- GET /api/v1/workspaces/{workspace_id}/tasks/{task_id}
- GET /api/v1/workspaces/{workspace_id}/repositories
- DELETE /api/v1/workspaces/{workspace_id}/repositories/{repository_id}

Repository registration currently accepts HTTPS GitHub repository URLs and records metadata only. It does not clone, fetch, or execute repository content. The connection status remains `pending_connection` until a GitHub App/OAuth authorization flow is implemented.

Passwords use Argon2 hashes. Access tokens are short-lived JWTs. Workspace and repository access is owner-scoped. Refresh/revocation, email verification, password reset, rate limiting, and account recovery are not implemented. This is an early development foundation, not production-ready identity/tenancy.

## Agent task persistence (early foundation)

Task creation is owner-scoped to a workspace and a repository registered in that same workspace. It creates a persisted task and attempt 1 with status `queued`. Task detail includes attempt and event history. Migration `0003_agent_tasks_and_approvals` adds task, attempt, event, and approval-request tables.

Only the deterministic `fake` engine profile is currently accepted by the task API. Tasks are **not dispatched or executed** yet; no repository is cloned and no shell/tool calls are run. Approval records are database groundwork only: decision endpoints, expiry enforcement, policy evaluation, and replay protection are still pending.
