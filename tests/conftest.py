import asyncio
import os
import pytest
from typing import AsyncGenerator

from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.infrastructure.api.main import app
from app.infrastructure.database.session import get_async_session
from app.config.settings import settings


# ---------------------------------------------------------
# TEST DATABASE URL (override production config)
# ---------------------------------------------------------
# Use a dedicated test DB; fallback to in-memory if missing
TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "sqlite+aiosqlite:///:memory:"
)


# ---------------------------------------------------------
# EVENT LOOP FOR ASYNC TESTS
# ---------------------------------------------------------
@pytest.fixture(scope="session")
def event_loop():
    """Create a session-wide event loop for asyncio tests."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


# ---------------------------------------------------------
# ASYNC ENGINE FIXTURE
# ---------------------------------------------------------
@pytest.fixture(scope="session")
async def async_engine():
    """Provide an async engine connected to the test DB."""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
        future=True,
    )
    yield engine
    await engine.dispose()


# ---------------------------------------------------------
# ASYNC SESSION FACTORY FIXTURE
# ---------------------------------------------------------
@pytest.fixture(scope="session")
async def async_session_factory(async_engine):
    """Create a session factory bound to the test engine."""
    return async_sessionmaker(
        bind=async_engine,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False,
        class_=AsyncSession,
    )


# ---------------------------------------------------------
# DATABASE SESSION FIXTURE (per test)
# ---------------------------------------------------------
@pytest.fixture
async def db_session(async_session_factory) -> AsyncGenerator[AsyncSession, None]:
    """
    Provide a fresh transactional database session for each test.

    Rolls back everything at the end so tests are isolated.
    """
    async with async_session_factory() as session:
        async with session.begin():
            yield session

        # Rollback to ensure each test has a clean state
        await session.rollback()


# ---------------------------------------------------------
# OVERRIDE DEPENDENCY: get_async_session
# ---------------------------------------------------------
@pytest.fixture
def override_get_async_session(db_session):
    """
    Override FastAPI dependency so routes use the test DB session.
    """

    async def _override():
        yield db_session

    app.dependency_overrides[get_async_session] = _override
    yield
    app.dependency_overrides.clear()


# ---------------------------------------------------------
# ASYNC FASTAPI CLIENT FIXTURE
# ---------------------------------------------------------
@pytest.fixture
async def client(override_get_async_session):
    """
    Provide an async test client with dependency overrides active.
    """
    transport = ASGITransport(app=app)
    
    async with AsyncClient(
        transport=transport,
        base_url="http://testserver"
    ) as ac:
        yield ac
