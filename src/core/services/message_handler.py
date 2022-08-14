import abc

from bots.interfaces import BotInterface


class MessageHandler(abc.ABC):
    def __init__(self, message: str, bot: BotInterface):
        self._message = message
        self._bot = bot

    @abc.abstractmethod
    def is_valid(self) -> bool:
        # We can use Regex or sending the message to WIT
        ...

    @abc.abstractmethod
    def handle(self):
        ...
