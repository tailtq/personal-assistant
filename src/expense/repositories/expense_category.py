from typing import Type

from mongoengine import Document

from core.repositories.base import BaseRepository
from ..models import ExpenseCategory


class ExpenseCategoryRepository(BaseRepository):
    @property
    def model(self) -> Type[Document]:
        return ExpenseCategory
