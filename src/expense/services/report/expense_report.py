from datetime import datetime

from typing import Optional, Type, Tuple, List

from expense.services import ExpenseService, ExpenseCategoryService
from expense.services.report.expense_report_chart import (
    ExpensePieChartService,
    ExpenseTableService,
    ExpensePlottingService,
    ExpenseImagePlottingService,
)


class ExpenseReportService:
    _MINIMUM_AMOUNT = 15

    def __init__(self, from_date: datetime, to_date: datetime, report_type: str):
        self._expense_service = ExpenseService()
        self._expense_category_service = ExpenseCategoryService()
        self._from_date = from_date
        self._to_date = to_date
        self._report_type = report_type

    def plot_chart(self) -> Tuple[Optional[str], Optional[str]]:
        # get expense items
        total_amount = self._expense_service.get_total_amount(self._from_date, self._to_date)
        if total_amount == 0:
            return None, None
        titles, amount = self._get_titles_and_amount()
        plotting_service = self._get_plotting_service()(titles, amount, total_amount, self._get_title(total_amount))
        content = plotting_service.plot()
        return content, self._get_plotting_type()

    def _get_plotting_service(self) -> Type[ExpensePlottingService]:
        """
        A Factory method to get plotting service
        """
        if self._report_type == "piechart":
            return ExpensePieChartService
        elif self._report_type == "table":
            return ExpenseTableService

    def _get_plotting_type(self) -> str:
        """
        Get plotting type
        """
        if issubclass(self._get_plotting_service(), ExpenseImagePlottingService):
            return "image"
        else:
            return "text"

    def _get_titles_and_amount(self) -> Tuple[List[str], List[float]]:
        """
        Get all expense titles and amount during a specific period
        """
        expense_items = self._expense_service.group_by_category(self._from_date, self._to_date, self._MINIMUM_AMOUNT)
        # map categories
        category_ids = [item["category"] for item in expense_items]
        categories = {
            category["id"]: category for category in self._expense_category_service.list({"id__in": category_ids})
        }
        titles = []
        amount = []
        for item in expense_items:
            titles.append(categories.get(item["category"]).title)
            amount.append(item["total_amount"])
        return titles, amount

    def _get_title(self, total_amount: float) -> str:
        """
        Get report title
        """
        from_date = self._from_date.strftime("%d/%m")
        to_date = self._to_date.strftime("%d/%m")
        total_amount = int(total_amount)
        return f"Expense ({from_date} - {to_date}): {total_amount}K VND"
