from fastapi import HTTPException, status


# ------------------------------------------------------------
# Base clean exception for all layers
# ------------------------------------------------------------
class AppError(Exception):
    """Base application-level exception."""
    pass


# ------------------------------------------------------------
# Domain-level errors (pure business logic)
# ------------------------------------------------------------
class DomainError(AppError):
    """Errors emerging from domain invariants."""
    pass


class EntityNotFoundError(DomainError):
    """A requested domain entity does not exist."""
    pass


class ValidationError(DomainError):
    """Domain value object or entity validation error."""
    pass


# ------------------------------------------------------------
# Application layer errors (use case failures)
# ------------------------------------------------------------
class UseCaseError(AppError):
    """Errors raised inside application use cases."""
    pass


class PermissionDeniedError(UseCaseError):
    """User does not have permission to perform an action."""
    pass


# ------------------------------------------------------------
# Infrastructure errors (database, adapters)
# ------------------------------------------------------------
class InfrastructureError(AppError):
    """Errors from database, network, and external providers."""
    pass


# ------------------------------------------------------------
# FastAPI translators — optional (used in app/main.py)
# ------------------------------------------------------------
def translate_exception(exc: AppError) -> HTTPException:
    """
    Map clean exceptions to FastAPI HTTP errors.
    """
    if isinstance(exc, EntityNotFoundError):
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc)
        )

    if isinstance(exc, PermissionDeniedError):
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exc)
        )

    if isinstance(exc, ValidationError):
        return HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc)
        )

    # Generic fallback
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=str(exc)
    )
