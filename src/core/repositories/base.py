from abc import ABC, abstractmethod
from typing import Type, List, Any, Optional, Union

from mongoengine import Document


class BaseRepository(ABC):
    @property
    @abstractmethod
    def model(self) -> Type[Document]:
        raise NotImplementedError()

    def list(self, conditions: dict, fields: Optional[list] = None) -> List[Any]:
        query = self.model.objects.filter(**conditions).all()
        query = query.only(*fields) if fields else query
        return query

    def first(self, **kwargs) -> Optional[Document]:
        return self.model.objects.filter(**kwargs).first()

    def create(self, data: Union[dict, list], load_multiple: bool = False) -> Optional[Document]:
        if type(data) == list:
            return self.model.objects.insert(data, load_bulk=load_multiple)
        return self.model.objects.create(**data)

    def update(self, conditions: dict, data: dict) -> Optional[Any]:
        return self.model.objects.filter(**conditions).update(**data)

    def save(self, instance: Document, data: dict) -> Document:
        for key, value in data.items():
            if key not in ["pk", "id", "created_at", "updated_at"]:
                setattr(instance, key, value)
        instance.save()
        return instance

    def delete(self, **kwargs) -> int:
        return self.model.objects.filter(**kwargs).delete()
