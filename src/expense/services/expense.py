from datetime import datetime
from typing import Union, Dict, List, Tuple

from bson import ObjectId

from core.services import BaseService
from .expense_category import ExpenseCategoryService
from ..models import Expense
from ..repositories import ExpenseRepository


class ExpenseService(BaseService):
    def __init__(self):
        super().__init__(ExpenseRepository)
        self.repository: ExpenseRepository
        self._expense_category_service = ExpenseCategoryService()

    def create_with_freetext_category(self, data: List[Dict[str, str]]) -> Tuple[List[ObjectId], datetime]:
        """
        Create expenses with free-text category
        """
        insert_data = []
        spent_at = None

        for item in data:
            # preprocess data
            item = {key: value.strip() for key, value in item.items()}
            # group freetext category
            category = self._expense_category_service.group_category(item["category"].strip())
            spent_at = datetime.strptime(f"{item['spent_at']}/{datetime.today().year}", "%d/%m/%Y")
            insert_data.append(
                Expense(
                    category=category,
                    description=item.get("description", "").strip(),
                    amount=float(item["amount"].strip()),
                    currency=self._group_currency(item["currency"].strip()),
                    spent_at=spent_at
                )
            )
        # insert multiple items
        result = self.repository.create(insert_data)
        return result, spent_at

    @staticmethod
    def _group_currency(currency: str):
        return "KVND" if currency.strip().lower() == "k" else "$"

    def _delete_relationships(self, _id: Union[str, int]):
        pass
