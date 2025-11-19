"""
Alembic Environment Configuration
Handles both async and sync database migrations.
"""
import sys
import pathlib

# Add project root to PYTHONPATH
BASE_DIR = pathlib.Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR))

from alembic import context
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool

# ---- Load application settings ----
from src.config.settings import Settings
settings = Settings()

# ---- Import SQLAlchemy Base and all models ----
# NOTE: These imports MUST stay here so Alembic can detect models.
from src.infrastructure.database.base import Base

# Import models from each slice so they register with Base.metadata
import src.infrastructure.database.models.academic.attendance_model  # noqa
import src.infrastructure.database.models.academic.grade_model  # noqa
import src.infrastructure.database.models.financial.invoice_model  # noqa
import src.infrastructure.database.models.financial.payment_model  # noqa
import src.infrastructure.database.models.administrative.student_model  # noqa
import src.infrastructure.database.models.administrative.schedule_model  # noqa

# ---- Alembic Config ----
config = context.config

# Override sqlalchemy.url dynamically
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


# --------------------------------------------------------------------------------------
# RUN Migrations Offline
# --------------------------------------------------------------------------------------
def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


# --------------------------------------------------------------------------------------
# RUN Migrations Online
# --------------------------------------------------------------------------------------
def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,            # detect column type changes
            compare_server_default=True,  # detect changes in defaults
            compare_nullable=True,        # detect nullability changes
        )

        with context.begin_transaction():
            context.run_migrations()


# ---- Run ----
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
