from logging.config import fileConfig
from sqlalchemy import create_engine
from sqlalchemy import pool
from sqlalchemy import text
from alembic import context

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

# Import your Base (contains metadata)
from src.infrastructure.database.base import Base
from src.config.settings import settings


# ---------------------------------------------------------
# 1. Alembic Config
# ---------------------------------------------------------
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# ---------------------------------------------------------
# 2. Convert ASYNC URL → SYNC URL for Alembic
# ---------------------------------------------------------
def get_sync_url(async_url: str) -> str:
    if async_url.startswith("postgresql+asyncpg://"):
        return async_url.replace(
            "postgresql+asyncpg://",
            "postgresql+psycopg2://",
            1
        )
    return async_url


sync_database_url = get_sync_url(settings.DATABASE_URL)


# ---------------------------------------------------------
# 3. Set metadata for autogeneration
# ---------------------------------------------------------
target_metadata = Base.metadata


# ---------------------------------------------------------
# 4. Offline migrations (no DB connection)
# ---------------------------------------------------------
def run_migrations_offline():
    context.configure(
        url=sync_database_url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


# ---------------------------------------------------------
# 5. Online migrations (real DB connection)
# ---------------------------------------------------------
def run_migrations_online():
    engine = create_engine(
        sync_database_url,
        poolclass=pool.NullPool,
        future=True
    )

    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


# ---------------------------------------------------------
# 6. Execute
# ---------------------------------------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
