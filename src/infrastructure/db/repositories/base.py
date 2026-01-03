from abc import ABCMeta
from typing import Any, Dict, Generic, List, Optional, Sequence, Type, TypeVar, Union
from fastapi_filter.base.filter import BaseFilterModel
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import Executable

from src.infrastructure.db.models.base import BaseORMModel
from src.infrastructure.db.mapper import Mapper

T = TypeVar('T', bound=BaseORMModel)
E = TypeVar('E')

class RepositoryMeta(ABCMeta):
    def __new__(mcls, name, bases, namespace, **kwargs):
        cls = super().__new__(mcls, name, bases, namespace, **kwargs)
        for base in getattr(cls, '__orig_bases__', ()):
            if hasattr(base, '__args__') and len(base.__args__) >= 2:
                cls.orm_model = base.__args__[0]
                cls.entity_model = base.__args__[1]
        return cls

class BaseRepository(Generic[T, E], metaclass=RepositoryMeta):
    orm_model: Type[T]
    entity_model: Type[E]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, entity: E) -> E:
        orm_obj = Mapper.to_orm(entity, self.orm_model)
        self.session.add(orm_obj)
        await self.session.commit()
        await self.session.refresh(orm_obj)
        return Mapper.to_domain(orm_obj, self.entity_model)

    async def get(self, id: Any, relations: Optional[Sequence[str]] = None) -> Optional[E]:
        stmt = select(self.orm_model).where(self.orm_model.id == id)
        if relations:
            stmt = stmt.options(*[selectinload(getattr(self.orm_model, r)) for r in relations])
        result = await self.session.execute(stmt)
        orm_obj = result.scalars().first()
        return Mapper.to_domain(orm_obj, self.entity_model)

    async def list(
        self,
        filters: Optional[Union[Dict[str, Any], BaseFilterModel]] = None,
        relations: Optional[Sequence[str]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> List[E]:
        stmt = select(self.orm_model)
        if relations:
            stmt = stmt.options(*[selectinload(getattr(self.orm_model, r)) for r in relations])
        if offset is not None:
            stmt = stmt.offset(offset)
        if limit is not None:
            stmt = stmt.limit(limit)
        
        stmt = self._apply_filters(stmt, filters)
        result = await self.session.execute(stmt)
        orm_objects = result.scalars().all()
        return [Mapper.to_domain(obj, self.entity_model) for obj in orm_objects]

    async def update(self, entity: E) -> Optional[E]:
        update_data = asdict(entity)
        obj_id = update_data.get('id')
        if obj_id is None:
            return None

        stmt = select(self.orm_model).where(self.orm_model.id == obj_id)
        result = await self.session.execute(stmt)
        orm_obj = result.scalars().first()
        
        if not orm_obj:
            return None

        for key, value in update_data.items():
            if key != 'id' and hasattr(orm_obj, key):
                setattr(orm_obj, key, value)
        
        await self.session.commit()
        await self.session.refresh(orm_obj)
        return Mapper.to_domain(orm_obj, self.entity_model)

    async def delete(self, id: Any) -> bool:
        stmt = select(self.orm_model).where(self.orm_model.id == id)
        result = await self.session.execute(stmt)
        orm_obj = result.scalars().first()
        if orm_obj:
            await self.session.delete(orm_obj)
            await self.session.commit()
            return True
        return False

    def _apply_filters(self, stmt: Executable, filters: Optional[Union[Dict[str, Any], BaseFilterModel]] = None) -> Executable:
        if not filters:
            return stmt
        if isinstance(filters, dict):
            for attr, value in filters.items():
                if hasattr(self.orm_model, attr):
                    stmt = stmt.where(getattr(self.orm_model, attr) == value)
        elif isinstance(filters, BaseFilterModel):
            stmt = filters.filter(stmt)
            stmt = filters.sort(stmt)
        return stmt

    async def count(self, filters: Optional[Union[Dict[str, Any], BaseFilterModel]] = None) -> int:
        stmt = select(func.count()).select_from(self.orm_model)
        stmt = self._apply_filters(stmt, filters)
        result = await self.session.execute(stmt)
        return result.scalar()