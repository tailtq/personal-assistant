import abc

from django.conf import settings

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
    async def handle(self):
        ...

    async def _respond(self, message: str):
        user_id = settings.DISCORD_USER_ID
        await self._bot.send_message(user_id, message)
