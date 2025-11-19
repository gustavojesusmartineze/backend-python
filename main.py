# main.py (project root)
import os
import uvicorn

from src.config.settings import settings

if __name__ == "__main__":
    # Use uvicorn programmatically so we can pass settings
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", "8000"))
    reload_flag = settings.APP_DEBUG

    uvicorn.run(
        "src.infrastructure.api.main:app",
        host=host,
        port=port,
        log_level="debug" if settings.APP_DEBUG else "info",
        reload=reload_flag,
    )
