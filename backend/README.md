# BuckLabs Dev API

Initial FastAPI control-plane skeleton.

## Requirements
- Python 3.11+
- A virtual environment

## Local setup (PowerShell)

```powershell
cd backend
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

Open:
- API health: http://127.0.0.1:8000/health
- OpenAPI docs: http://127.0.0.1:8000/docs

## Current scope
- Application factory and health/readiness endpoints.
- Typed environment configuration.
- No unauthenticated workspace CRUD.
- No code execution, shell tool, repository write, or sandbox capability is implemented yet.

Readiness currently reports service process/configuration status only. It does not claim that external infrastructure is connected.
