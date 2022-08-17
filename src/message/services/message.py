from functools import wraps
from typing import Union, Optional, Dict

from core.services import BaseService
from ..const import MessageTemplate
from ..repositories.message import MessageRepository


class MessageService(BaseService):
    def __init__(self):
        super().__init__(MessageRepository)

    def get_user_context(self, user_id: str) -> Optional[Dict]:
        message = self.repository.first(user_id=user_id)
        return message.context if message else None

    def _delete_relationships(self, _id: Union[str, int]):
        ...


def save_message(app_name: str):
    message_service = MessageService()

    def wrapper(func):
        @wraps(func)
        async def decorator(self):
            message_data = {
                "user_id": self._user_id,
                "app_name": app_name,
                "human_text": self._message,
                "nlu_result": self._nlu_result,
                "context": self._context,
            }
            try:
                response: str = await func(self)
                message_service.create({
                    **message_data,
                    "bot_text": response,
                })
                return response
            except Exception as e:
                message_service.create({
                    **message_data,
                    "bot_text": MessageTemplate.TECHNICAL_ISSUE,
                })
                raise e

        return decorator

    return wrapper
