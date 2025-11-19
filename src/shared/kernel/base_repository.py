from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List

T = TypeVar("T")      # Entity type
ID = TypeVar("ID")    # ID type (UUID usually)


class BaseRepository(ABC, Generic[T, ID]):
    """
    Abstract repository definition for all vertical slices.
    """

    @abstractmethod
    async def get_by_id(self, entity_id: ID) -> Optional[T]:
        raise NotImplementedError

    @abstractmethod
    async def save(self, entity: T) -> T:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, entity_id: ID) -> None:
        raise NotImplementedError

    async def list(self, limit: int = 100, offset: int = 0) -> List[T]:
        """
        Optional convenience method.
        Concrete repositories may override for efficiency.
        """
        raise NotImplementedError("list() not implemented")
