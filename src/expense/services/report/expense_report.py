from datetime import datetime

import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, Optional

from expense.services import ExpenseService, ExpenseCategoryService


class ExpenseReportService:
    _MINIMUM_AMOUNT = 15

    def __init__(self, from_date: datetime, to_date: datetime):
        self._expense_service = ExpenseService()
        self._expense_category_service = ExpenseCategoryService()
        self._from_date = from_date
        self._to_date = to_date

    def plot_pie_chart(self, chart_path: str) -> Optional[str]:
        # get expense items
        total_amount = self._expense_service.get_total_amount(self._from_date, self._to_date)
        if total_amount == 0:
            return None
        expense_items = self._expense_service.group_by_category(self._from_date, self._to_date, self._MINIMUM_AMOUNT)
        # map categories
        category_ids = [item["category"] for item in expense_items]
        categories = {
            category["id"]: category for category in self._expense_category_service.list({"id__in": category_ids})
        }
        for item in expense_items:
            item["category"] = categories.get(item["category"])

        # calculate chart's specification
        labels = [self._get_label(item) for item in expense_items]
        sizes = [item["total_amount"] / total_amount * 100 for item in expense_items]
        colors = sns.set_palette("Spectral")
        # plot expenses into a pie chart and save to an image file
        plt.pie(sizes, labels=labels, colors=colors, autopct="%.0f%%", startangle=90)
        plt.axis("equal")
        # set title
        from_date = self._from_date.strftime("%d/%m")
        to_date = self._to_date.strftime("%d/%m")
        total_amount = int(total_amount)
        plt.title(f"Expense ({from_date} - {to_date}): {total_amount}K VND", pad=20)
        # save figure
        plt.savefig(chart_path)
        return chart_path

    @staticmethod
    def _get_label(expense_item: Dict) -> str:
        category_title = expense_item["category"].title
        total_amount = int(expense_item["total_amount"])
        return f"{category_title} ({total_amount}K)"
