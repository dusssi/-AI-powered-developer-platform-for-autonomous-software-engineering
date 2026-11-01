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

Passwords use Argon2 hashes. Access tokens are short-lived JWTs. Workspace access is owner-scoped. Refresh/revocation, email verification, password reset, rate limiting, and account recovery are not implemented. This is an early development foundation, not production-ready identity/tenancy.
