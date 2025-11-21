from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.infrastructure.database.session import get_async_session

router = APIRouter()

@router.get("/health", tags=["health"])
async def health(db: AsyncSession = Depends(get_async_session)):
    """
    Simple health check that verifies DB connectivity.
    Returns 200 {"status":"ok"} if DB responds.
    """
    try:
        await db.execute(text("SELECT 1"))
        return {"status": "ok"}
    except Exception as exc:
        # Do not leak internal error details in production
        return {"status": "error", "detail": str(exc)}