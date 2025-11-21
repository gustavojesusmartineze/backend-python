from typing import Any, Dict, Optional
import logging

from src.config.settings import settings
from src.infrastructure.database import session as db_session

logger = logging.getLogger(__name__)


class Container:
    """
    Lightweight application container.
    Stores references to shared services and factories.
    """

    def __init__(self):
        # core shared objects
        self.settings = settings
        self._singletons: Dict[str, Any] = {}
        self._initialized = False

    # -------------------------
    # Bootstrapping
    # -------------------------
    def initialize(self, *, echo: bool = False) -> None:
        """
        Initialize container resources (engines, sessions, adapters).
        Idempotent.
        """
        if self._initialized:
            return
        # Initialize DB engines/session factories
        db_session.init_engines(echo=echo)
        # Store engines for convenience
        self._singletons["async_engine"] = db_session.get_async_engine()
        self._singletons["sync_engine"] = db_session.get_sync_engine()
        # Could initialize other adapters here (S3 clients, payment clients...)
        self._initialized = True
        logger.info("Container initialized.")

    # -------------------------
    # Registration helpers
    # -------------------------
    def register(self, name: str, instance: Any) -> None:
        self._singletons[name] = instance

    def resolve(self, name: str) -> Any:
        try:
            return self._singletons[name]
        except KeyError as exc:
            raise RuntimeError(f"Dependency '{name}' not registered in container.") from exc

    # -------------------------
    # Convenience accessors
    # -------------------------
    @property
    def async_engine(self):
        return self._singletons.get("async_engine")

    @property
    def sync_engine(self):
        return self._singletons.get("sync_engine")


# Single global container instance (import this)
container = Container()
