import re

from message.dtos import MessageDTO
from message.services.message import save_message
from message.services.handlers.message_handler import MessageHandler
from expense.services import ExpenseService
from message.const import AppName, MessageTemplate


class ExpenseMessageHandler(MessageHandler):
    VALID_PATTERN: str = r"\d+\/\d+ ([a-zA-Z\+ ]+ \d+(k|\$)?( \([\w ]+\))?,?)+"
    EXTRACT_DATE_PATTERN: str = r"\d+\/\d+"
    EXTRACT_EXPENSES_PATTERN: str = r" ?([a-zA-Z\+ ]+) (\d+)(k|\$)?(?: \(([\w ]+)\))?"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._expense_service = ExpenseService()

    def is_valid(self) -> bool:
        return bool(re.fullmatch(self.VALID_PATTERN, self._message))

    @save_message(AppName.EXPENSE)
    def handle(self) -> MessageDTO:
        """
        Add expense to database and respond back to the client.
        If it couldn't detect any expense, an error message will be sent back.
        """
        date = re.search(self.EXTRACT_DATE_PATTERN, self._message)
        expense_items = re.findall(self.EXTRACT_EXPENSES_PATTERN, self._message[date.end() + 1:])
        for i, item in enumerate(expense_items):
            expense_items[i] = {
                "spent_at": date.group(0),
                "title": item[0],
                "amount": item[1],
                "currency": item[2],
                "description": item[3],
            }
        if expense_items:
            _, spent_at = self._expense_service.create_with_freetext_category(expense_items)
            message = MessageTemplate.EXPENSE_ADDED.format(date=spent_at.strftime("%d/%m"))
        else:
            message = MessageTemplate.EXPENSE_MISSING
        return MessageDTO(message)
