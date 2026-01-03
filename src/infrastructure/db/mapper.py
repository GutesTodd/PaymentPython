from dataclasses import asdict, fields
from typing import Type, TypeVar, Any
from src.infrastructure.db.models.base import BaseORMModel

E = TypeVar("E")  # Entity
T = TypeVar("T", bound=BaseORMModel)  # ORM Model

class Mapper:
    @staticmethod
    def to_domain(orm_obj: Any, domain_class: Type[E]) -> E:
        if orm_obj is None:
            return None

        data = {
            field.name: getattr(orm_obj, field.name) 
            for field in fields(domain_class) 
            if hasattr(orm_obj, field.name)
        }
        return domain_class(**data)

    @staticmethod
    def to_orm(domain_obj: E, orm_class: Type[T]) -> T:
        if domain_obj is None:
            return None
            
        data = asdict(domain_obj)
        clean_data = {k: v for k, v in data.items() if v is not None}
        return orm_class(**clean_data)