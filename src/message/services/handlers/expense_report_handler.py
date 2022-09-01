import re
from datetime import datetime

from expense.services.report import ExpenseReportService
from message.dtos import MessageDTO
from message.services.message import save_message
from message.services.handlers.message_handler import MessageHandler
from message.const import AppName, MessageTemplate


class ExpenseReportHandler(MessageHandler):
    VALID_PATTERN: str = r"(?:Report|report) (\d+\/\d+) - (\d+\/\d+)"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def is_valid(self) -> bool:
        return bool(re.fullmatch(self.VALID_PATTERN, self._message))

    @save_message(AppName.EXPENSE)
    def handle(self) -> MessageDTO:
        """
        Add expense to database and respond back to the client.
        If it couldn't detect any expense, an error message will be sent back.
        """
        year = datetime.today().year
        from_date, to_date = re.fullmatch(self.VALID_PATTERN, self._message).groups()
        from_date = datetime.strptime(from_date, "%d/%m").replace(year=year)
        to_date = datetime.strptime(to_date, "%d/%m").replace(year=year)

        report_img_path = "test.jpg"
        report_service = ExpenseReportService(from_date, to_date)
        result = report_service.plot_pie_chart(report_img_path)
        if result is None:
            return MessageDTO(MessageTemplate.EXPENSE_REPORTED_FAILED)
        return MessageDTO(MessageTemplate.EXPENSE_REPORTED, [report_img_path])
