from typing import Type

from mongoengine import Document

from core.repositories.base import BaseRepository
from ..models import Expense


class ExpenseRepository(BaseRepository):
    @property
    def model(self) -> Type[Document]:
        return Expense
