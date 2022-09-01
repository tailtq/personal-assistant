from typing import Type
from datetime import datetime

from mongoengine import Document

from core.repositories.base import BaseRepository
from ..models import Expense


class ExpenseRepository(BaseRepository):
    @property
    def model(self) -> Type[Document]:
        return Expense

    def group_by_category(self, from_date: datetime, to_date: datetime, minimum_amount: float = 0):
        """
        Group expenses having the same category together
        """
        return list(self.model.objects.aggregate([
            {
                "$match": {
                    "spent_at": {
                        "$gte": from_date,
                        "$lte": to_date,
                    }
                }
            },
            {
                "$group": {
                    "_id": "$category",
                    "total_amount": {
                        "$sum": "$amount"
                    },
                    "spent_at": {
                        "$push": "$spent_at"
                    }
                },
            },
            {
                "$match": {
                    "total_amount": {
                        "$gte": minimum_amount,
                    }
                }
            },
            {
                "$sort": {
                    "total_amount": 1,
                },
            },
            {
                "$project": {
                    "_id": None,
                    "category": "$_id",
                    "total_amount": "$total_amount",
                    "spent_at": "$spent_at",
                }
            },
        ]))

    def get_total_amount(self, from_date: datetime, to_date: datetime) -> float:
        """
        Get total expense in a period
        """
        return self.model.objects.filter(spent_at__gte=from_date, spent_at__lte=to_date).sum("amount")
