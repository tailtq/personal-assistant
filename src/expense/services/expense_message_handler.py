import re
from re import Pattern

from core.services.message_handler import MessageHandler


class ExpenseMessageHandler(MessageHandler):
    PATTERN: Pattern = r"\d+\/\d+ ([a-zA-Z ]+ \d+(k|\$)?,?)+"

    def is_valid(self) -> bool:
        return bool(re.fullmatch(self.PATTERN, self._message))

    def handle(self):
        date = re.match(r"\d+\/\d+", self._message)
        expense_items = re.findall(r"([a-zA-Z ]+) (\d+)(k|\$)?", self._message)

        for item in expense_items:
            pass
        pass
