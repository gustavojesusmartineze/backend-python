from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.session import get_async_session
from app.config.container import container


async def get_db_session() -> AsyncSession:
    """
    Provides an AsyncSession for FastAPI endpoints.
    """
    async for session in get_async_session():
        yield session


def get_container():
    """
    Provides the global DI container instance.
    """
    return container


# Example placeholder for authentication (to be implemented later)
async def get_current_user():
    """
    Placeholder for auth system. 
    Replace with JWT or session-based authentication.
    """
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Authentication not configured.",
    )
