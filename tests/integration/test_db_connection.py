import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.integration
async def test_database_connection(db_session: AsyncSession):
    """
    Verify that the database session can:
    - Open a connection
    - Execute a simple SQL statement
    - Return the expected result
    """
    result = await db_session.execute(text("SELECT 1"))
    value = result.scalar()

    assert value == 1, "Database did not return expected value from SELECT 1"
