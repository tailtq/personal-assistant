import abc
from typing import List

import matplotlib.pyplot as plt
import seaborn as sns
from prettytable import PrettyTable


class ExpensePlottingService(abc.ABC):
    def __init__(self, titles: List[str], amount: List[float], total_amount: float, report_title: str):
        self._titles = titles
        self._amount = amount
        self._total_amount = total_amount
        self._report_title = report_title

    @abc.abstractmethod
    def plot(self):
        pass

    @staticmethod
    def _get_amount(amount: float):
        return f"{int(amount)}K"


class ExpenseImagePlottingService(ExpensePlottingService):
    ...


class ExpenseTextPlottingService(ExpensePlottingService):
    ...


class ExpensePieChartService(ExpenseImagePlottingService):
    def plot(self) -> str:
        labels = [self._get_label(title, amount) for title, amount in zip(self._titles, self._amount)]
        sizes = [item / self._total_amount * 100 for item in self._amount]
        colors = sns.set_palette("Spectral")
        # plot expenses into a pie chart and save to an image file
        plt.pie(sizes, labels=labels, colors=colors, autopct="%.0f%%", startangle=90)
        plt.axis("equal")
        plt.title(self._report_title, pad=20)
        # save figure
        chart_path = "test.jpg"
        plt.savefig(chart_path)
        plt.close()
        return chart_path

    @classmethod
    def _get_label(cls, title: str, amount: float) -> str:
        return f"{title} ({cls._get_amount(amount)})"


class ExpenseTableService(ExpenseTextPlottingService):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._titles = list(reversed(self._titles))
        self._amount = list(reversed(self._amount))

    def plot(self) -> str:
        table = PrettyTable(align="l", title=self._report_title)
        table.field_names = ["", "Title", "Amount (VND)"]
        for i, (title, amount) in enumerate(zip(self._titles, self._amount)):
            index = str(i + 1).rjust(len(str(len(self._titles))), "0")
            amount = self._get_amount(amount)
            table.add_row([index, title, amount])
        return table.get_string()
