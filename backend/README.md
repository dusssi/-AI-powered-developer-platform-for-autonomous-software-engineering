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
- GET /api/v1/workspaces/{workspace_id}/repositories
- DELETE /api/v1/workspaces/{workspace_id}/repositories/{repository_id}

Repository registration accepts HTTPS GitHub repository URLs and records metadata only. The GitHub App installation handshake is available when `GITHUB_APP_SLUG` and `GITHUB_WEBHOOK_SECRET` are configured. Set the GitHub App Setup URL to `/api/v1/github/setup/callback` and its webhook URL to `/api/v1/github/webhook`; subscribe to the `installation` event. The callback uses a one-time, expiring state value. Webhooks are authenticated with HMAC-SHA256. This records installation metadata only: it does not yet mint installation access tokens, enumerate repositories, clone code, or index source files.

Passwords use Argon2 hashes. Access tokens are short-lived JWTs. Workspace and repository access is owner-scoped. Refresh/revocation, email verification, password reset, rate limiting, and account recovery are not implemented. This is an early development foundation, not production-ready identity/tenancy.
