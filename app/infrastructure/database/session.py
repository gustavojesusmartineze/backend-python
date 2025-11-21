from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.infrastructure.database.base import Base
from src.config.settings import settings


# ---------------------------------------------------------------------
# ASYNC ENGINE (Primary runtime)
# ---------------------------------------------------------------------
_ASYNC_ENGINE: AsyncEngine | None = None
async_session: async_sessionmaker[AsyncSession] | None = None


def get_async_engine() -> AsyncEngine:
    """Lazy-initialize the async SQLAlchemy engine."""
    global _ASYNC_ENGINE, async_session

    if _ASYNC_ENGINE is None:
        _ASYNC_ENGINE = create_async_engine(
            settings.DATABASE_URL,
            echo=settings.DB_ECHO,
            future=True,
            pool_pre_ping=True,
        )

        async_session = async_sessionmaker(
            bind=_ASYNC_ENGINE,
            expire_on_commit=False,
            autoflush=False,
            autocommit=False,
        )

    return _ASYNC_ENGINE


# ---------------------------------------------------------------------
# SYNC ENGINE (Used for Alembic or scripts)
# ---------------------------------------------------------------------
_SYNC_ENGINE = None


def get_sync_engine():
    """Sync engine for Alembic / scripts only."""
    global _SYNC_ENGINE

    if _SYNC_ENGINE is None:
        sync_url = settings.DATABASE_URL

        # convert asyncpg -> psycopg2
        if sync_url.startswith("postgresql+asyncpg://"):
            sync_url = sync_url.replace(
                "postgresql+asyncpg://", "postgresql+psycopg2://", 1
            )

        _SYNC_ENGINE = create_engine(
            sync_url,
            echo=settings.DB_ECHO,
            future=True,
            pool_pre_ping=True,
        )

    return _SYNC_ENGINE


# ---------------------------------------------------------------------
# FastAPI Dependency: get_async_session
# ---------------------------------------------------------------------
async def get_async_session() -> AsyncSession:
    """Provide an async SQLAlchemy session for FastAPI route dependencies."""
    if async_session is None:
        get_async_engine()  # initialize factory

    async with async_session() as session:
        yield session


# ---------------------------------------------------------------------
# Helper for synchronous scripts (rarely used)
# ---------------------------------------------------------------------
def get_sync_session() -> Session:
    engine = get_sync_engine()
    return Session(bind=engine, expire_on_commit=False)
