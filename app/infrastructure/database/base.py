from sqlalchemy.orm import DeclarativeBase, declared_attr
from sqlalchemy import MetaData, Column, DateTime, func
import uuid
from sqlalchemy.dialects.postgresql import UUID


# Naming convention helps Alembic produce consistent migrations
NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=NAMING_CONVENTION)


# ------------------------------------------------------------
# Common Mixins
# ------------------------------------------------------------

class UUIDPrimaryKeyMixin:
    """Adds a UUID primary key called 'id'."""
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
        index=True,
    )


class TimestampMixin:
    """Adds created_at and updated_at timestamp columns."""
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
