import re
from re import Pattern

from core.services.message_handler import MessageHandler
from expense.services import ExpenseService
from message.const import MESSAGES


class ExpenseMessageHandler(MessageHandler):
    VALID_PATTERN: str = r"\d+\/\d+ ([a-zA-Z ]+ \d+(k|\$)?( \([\w ]+\))?,?)+"
    EXTRACT_DATA_PATTERN: str = r"([a-zA-Z ]+) (\d+)(k|\$)?(?: \(([\w ]+)\))?"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._expense_service = ExpenseService()

    def is_valid(self) -> bool:
        return bool(re.fullmatch(self.VALID_PATTERN, self._message))

    async def handle(self):
        date = re.search(r"\d+\/\d+", self._message)
        expense_items = re.findall(self.EXTRACT_DATA_PATTERN, self._message[date.end() + 1:])
        for i, item in enumerate(expense_items):
            expense_items[i] = {
                "spent_at": date.group(0),
                "category": item[0],
                "amount": item[1],
                "currency": item[2],
                "description": item[3],
            }
        if expense_items:
            _, spent_at = self._expense_service.create_with_freetext_category(expense_items)
            await self._respond(MESSAGES["EXPENSE_ADDED"].format(date=spent_at.strftime("%d/%m")))
