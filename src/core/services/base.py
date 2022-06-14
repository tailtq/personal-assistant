from abc import ABC, abstractmethod
from typing import Type, List, Optional, Any

from mongoengine import Document


class BaseService(ABC):
    @property
    @abstractmethod
    def model(self) -> Type[Document]:
        raise NotImplementedError()

    def list(self, **kwargs) -> List[Any]:
        return self.model.objects.filter(**kwargs).all()

    def first(self, **kwargs) -> Optional[Any]:
        return self.model.objects.filter(**kwargs).first()

    def create(self, **kwargs) -> Optional[Any]:
        return self.model.objects.create(**kwargs)
