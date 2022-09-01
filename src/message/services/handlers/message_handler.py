import abc
from typing import Optional, Dict

from message.services.message import MessageService
from message.dtos import MessageDTO


class MessageHandler(abc.ABC):
    def __init__(self, message: str, user_id: int, context, prev_context: Optional[Dict]):
        self._message = message
        self._nlu_result = None
        self._user_id = user_id
        self._context = context
        self._prev_context = prev_context
        self._message_service = MessageService()

    @abc.abstractmethod
    def is_valid(self) -> bool:
        # We can use Regex or sending the message to WIT
        ...

    @abc.abstractmethod
    def handle(self) -> MessageDTO:
        ...
