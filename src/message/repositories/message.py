from typing import Type

from mongoengine import Document

from core.repositories.base import BaseRepository
from ..models import Message


class MessageRepository(BaseRepository):
    @property
    def model(self) -> Type[Document]:
        return Message
