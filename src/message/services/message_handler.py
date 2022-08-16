import abc

from django.conf import settings

from bots.interfaces import BotInterface


class MessageHandler(abc.ABC):
    def __init__(self, message: str):
        self._message = message
        self._nlu_result = None

    @abc.abstractmethod
    def is_valid(self) -> bool:
        # We can use Regex or sending the message to WIT
        ...

    @abc.abstractmethod
    async def handle(self) -> str:
        ...
