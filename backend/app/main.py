from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.health import router as health_router
from app.core.config import get_settings


def create_app() -> FastAPI:
    settings = get_settings()
    application = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        docs_url="/docs" if settings.expose_docs else None,
        redoc_url="/redoc" if settings.expose_docs else None,
        openapi_url="/openapi.json" if settings.expose_docs else None,
    )
    application.state.settings = settings

    if settings.cors_origins:
        application.add_middleware(
            CORSMiddleware,
            allow_origins=settings.cors_origins,
            allow_credentials=False,
            allow_methods=["GET"],
            allow_headers=["Content-Type", "Authorization"],
        )

    application.include_router(health_router)
    return application


app = create_app()
