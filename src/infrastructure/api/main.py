from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
import logging

from src.config.settings import settings
from src.infrastructure.database import session as db_session

# Import routers (these files may be placeholders initially)
from src.infrastructure.api.routers import (
    academic_router,
    financial_router,
    administrative_router,
    communication_router,
    health as health_router,
)

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """
    Application factory. Use this when running uvicorn or for tests.
    """
    app = FastAPI(
        title=settings.APP_NAME,
        debug=settings.APP_DEBUG,
        version="0.1.0",
    )

    # --------------------------------------------------------
    # Middleware
    # --------------------------------------------------------
    app.add_middleware(GZipMiddleware, minimum_size=500)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"] if settings.APP_DEBUG else [],  # restrict in prod
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # --------------------------------------------------------
    # Routers: keep slice routers small and imported from slice api/router modules
    # Each file should expose `router` (fastapi.APIRouter)
    # --------------------------------------------------------
    # We register a top-level prefix per high-level domain
    try:
        app.include_router(academic_router.router, prefix="/api/academic", tags=["academic"])
    except Exception as exc:
        logger.debug("Academic router not yet available: %s", exc)

    try:
        app.include_router(financial_router.router, prefix="/api/financial", tags=["financial"])
    except Exception as exc:
        logger.debug("Financial router not yet available: %s", exc)

    try:
        app.include_router(administrative_router.router, prefix="/api/admin", tags=["administrative"])
    except Exception as exc:
        logger.debug("Admin router not yet available: %s", exc)

    try:
        app.include_router(communication_router.router, prefix="/api/communication", tags=["communication"])
    except Exception as exc:
        logger.debug("Communication router not yet available: %s", exc)

    try:
        app.include_router(health_router.router, prefix="/api", tags=["health"])
    except Exception as exc:
        logger.debug("Health router not available: %s", exc)

    # --------------------------------------------------------
    # Startup / Shutdown events
    # --------------------------------------------------------
    @app.on_event("startup")
    async def on_startup():
        # Initialize DB engines / session factories
        from src.infrastructure.database.session import get_async_engine
        get_async_engine()
        logger.info("Engines initialized.")

    @app.on_event("shutdown")
    async def on_shutdown():
        # Properly dispose async engine to close connection pool
        try:
            engine = db_session.get_async_engine()
            await engine.dispose()
            logger.info("Async engine disposed.")
        except Exception as exc:
            logger.debug("Error disposing engine: %s", exc)

    return app


# Expose the app for uvicorn: `uvicorn src.infrastructure.api.main:app --reload`
app = create_app()
