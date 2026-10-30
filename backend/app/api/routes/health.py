from fastapi import APIRouter, Request, status

router = APIRouter(tags=["system"])


@router.get("/health", status_code=status.HTTP_200_OK)
async def health() -> dict[str, str]:
    """Liveness probe; indicates that the API process is responsive."""
    return {"status": "ok"}


@router.get("/ready", status_code=status.HTTP_200_OK)
async def readiness(request: Request) -> dict[str, str]:
    """Process readiness only; external dependencies are added to this check later."""
    settings = request.app.state.settings
    return {
        "status": "ready",
        "service": settings.app_name,
        "environment": settings.environment,
    }
