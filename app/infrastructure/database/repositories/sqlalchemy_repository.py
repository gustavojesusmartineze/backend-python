from typing import Type, Generic, TypeVar, Optional, List, Callable
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from src.shared.kernel.base_repository import BaseRepository
from src.shared.exceptions import EntityNotFoundError, InfrastructureError

T = TypeVar("T")       # Domain Entity
M = TypeVar("M")       # ORM Model
ID = TypeVar("ID")     # ID type


class SQLAlchemyRepository(BaseRepository[T, ID], Generic[T, M, ID]):
    """
    Generic async SQLAlchemy repository.

    Concrete slices should subclass this and provide:
    - model_cls: ORM model class
    - to_domain(model) -> T
    - to_model(entity) -> ORM model
    """

    model_cls: Type[M]
    to_domain: Callable[[M], T]
    to_model: Callable[[T], M]

    def __init__(self, session: AsyncSession):
        self.session = session

    # ------------------------------------------
    # GET BY ID
    # ------------------------------------------
    async def get_by_id(self, entity_id: ID) -> Optional[T]:
        stmt = select(self.model_cls).where(self.model_cls.id == entity_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if not model:
            return None
        return self.to_domain(model)

    # ------------------------------------------
    # LIST
    # ------------------------------------------
    async def list(self, limit: int = 100, offset: int = 0) -> List[T]:
        stmt = select(self.model_cls).limit(limit).offset(offset)
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self.to_domain(m) for m in models]

    # ------------------------------------------
    # SAVE (insert or update)
    # ------------------------------------------
    async def save(self, entity: T) -> T:
        try:
            model = self.to_model(entity)
            self.session.add(model)
            await self.session.commit()
            await self.session.refresh(model)
            return self.to_domain(model)
        except Exception as exc:
            await self.session.rollback()
            raise InfrastructureError(str(exc)) from exc

    # ------------------------------------------
    # DELETE
    # ------------------------------------------
    async def delete(self, entity_id: ID) -> None:
        stmt = delete(self.model_cls).where(self.model_cls.id == entity_id)
        await self.session.execute(stmt)
        await self.session.commit()
