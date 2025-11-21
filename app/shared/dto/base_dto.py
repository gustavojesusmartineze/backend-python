from pydantic import BaseModel, ConfigDict
from typing import Any, Type, TypeVar, Dict

T = TypeVar("T", bound="BaseDTO")


class BaseDTO(BaseModel):
    """
    BaseDTO is the shared parent class for all Request/Response DTOs.
    It ensures strict validation, clean serialization, and optional
    mapping utilities when converting from Domain Entities.
    """

    model_config = ConfigDict(
        from_attributes=True,   # Allows constructing DTOs from ORM/domain objects
        populate_by_name=True,  # Use aliases transparently
        extra="forbid",         # No unexpected fields allowed
        strict=True             # Strict type validation everywhere
    )

    @classmethod
    def from_entity(cls: Type[T], entity: Any) -> T:
        """
        Create a DTO from a domain entity or ORM model.
        This works because from_attributes=True is enabled.
        """
        return cls.model_validate(entity)

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize safely to a native dict.
        """
        return self.model_dump()
