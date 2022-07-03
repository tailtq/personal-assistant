from abc import ABC, abstractmethod
from typing import Type, List, Optional, Any, Union

from mongoengine import Document

from core.repositories.base import BaseRepository


class BaseService(ABC):
    def __init__(self, repository_class: Type[BaseRepository]):
        self.repository = repository_class()

    def list(self, conditions: Optional[dict] = None, fields: Optional[list] = None) -> List[Any]:
        return self.repository.list(conditions or {}, fields)

    def first(self, **kwargs) -> Optional[Any]:
        return self.repository.first(**kwargs)

    def get_by_id(self, _id: Optional[Union[str, int]]) -> Optional[Any]:
        return self.repository.first(pk=_id)

    def create(self, data: dict) -> Optional[Any]:
        return self.repository.create(data)

    def update(self, conditions: dict, data: dict) -> Optional[Any]:
        return self.repository.update(conditions, data)

    def save(self, instance: Document, data: dict) -> Document:
        return self.repository.save(instance, data)

    def delete_by_id(self, _id: Union[str, int]) -> int:
        self._delete_relationships(_id)
        return self.repository.delete(pk=_id)

    def delete(self, **kwargs) -> int:
        return self.repository.delete(**kwargs)

    @abstractmethod
    def _delete_relationships(self, _id: Union[str, int]):
        raise NotImplementedError()
