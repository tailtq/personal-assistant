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
            category = self._expense_category_service.group_category(item["title"])
            description = item.get("description", "")
            spent_at = datetime.strptime(f"{item['spent_at']}/{datetime.today().year}", "%d/%m/%Y")
            insert_data.append(
                Expense(
                    category=category,
                    description=item["title"] + (" (" + description + ")" if description else ""),
                    amount=float(item["amount"]),
                    currency=self._group_currency(item["currency"]),
                    spent_at=spent_at
                )
            )
        # insert multiple items
        result = self.repository.create(insert_data)
        return result, spent_at

    def group_by_category(self, from_date: datetime, to_date: datetime, minimum_amount: float = 0) -> List[Dict]:
        """
        Group all expenses having the same category together
        """
        return self.repository.group_by_category(from_date, to_date, minimum_amount)

    def get_total_amount(self, from_date: datetime, to_date: datetime) -> float:
        """
        Get total amount during a period
        """
        return self.repository.get_total_amount(from_date, to_date)

    @staticmethod
    def _group_currency(currency: str):
        return "$" if currency.strip() == "$" else "KVND"

    def _delete_relationships(self, _id: Union[str, int]):
        pass
