from typing import Union

from core.services import BaseService
from ..models import ExpenseCategory
from ..repositories import ExpenseCategoryRepository


class ExpenseCategoryService(BaseService):
    def __init__(self):
        super().__init__(ExpenseCategoryRepository)
        self.repository: ExpenseCategoryRepository

    def group_category(self, category_text: str) -> ExpenseCategory:
        result: ExpenseCategory = self.repository.first(title__iexact=category_text)
        if not result:
            result = self.repository.create({"title": category_text})
        return result

    def _delete_relationships(self, _id: Union[str, int]):
        pass
