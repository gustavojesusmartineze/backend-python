import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from src.infrastructure.database.session import get_async_engine, async_session


@pytest.mark.asyncio
async def test_database_connection_integration():
    """
    Integration test to verify that the application can create a DB engine,
    open a session, and execute a basic SQL query.
    """
    engine = get_async_engine()

    # Create a session manually for integration tests
    SessionLocal = async_session

    async with SessionLocal() as session:  # type: AsyncSession
        result = await session.execute(text("SELECT 1"))
        row = result.scalar()

        assert row == 1
