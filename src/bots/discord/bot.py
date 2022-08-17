from typing import Union, List, Type, Optional

import discord
import sentry_sdk
from discord import Embed
from discord.ext.commands import Bot, Cog
from django.conf import settings

from bots.base import BaseBot
from bots.interfaces import BotInterface
from message.services import ExpenseMessageHandler, MessageHandler, MessageService
from message.const import MessageTemplate


class DiscordBot(BaseBot, Bot, BotInterface):
    MESSAGE_EMBEDDED_COLOR = 0x0099ff

    def __init__(self, token: str, cog_classes: List[Type[Cog]] = None):
        BaseBot.__init__(self, token, command_prefix="")
        self._add_cogs(cog_classes)

    @property
    def message_handlers(self) -> List[Type[MessageHandler]]:
        return [
            ExpenseMessageHandler
        ]

    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return
        # message.content == 'raise-exception'
        # get intent -> handle relevant app
        # Note: All Discord messages must be sent via a channel (public, private)
        try:
            user_id = settings.DISCORD_USER_ID
            prev_context = MessageService().get_user_context(user_id)
            context = {}
            # Loop through handlers, determine the right one, and process
            for handler_class in self.message_handlers:
                handler = handler_class(message.clean_content, user_id, context, prev_context)
                if handler.is_valid():
                    response = await handler.handle()
                    await self.send_message(user_id, response)
                    break
        except Exception as e:
            await self.send_message(settings.DISCORD_USER_ID, MessageTemplate.TECHNICAL_ISSUE)
            sentry_sdk.capture_exception(e)

    async def on_ready(self):
        print(f"{self.user} is ready!")

    async def on_error(self, event, *args, **kwargs):
        raise

    async def send_message(self, user: Union[int, discord.User], message: Union[str, discord.Embed]) -> None:
        """
        Send a text message to a particular user
        """
        if type(user) != discord.User:
            user = await self.fetch_user(user)

        if type(message) == str:
            await user.send(content=message)
        elif type(message) == discord.Embed:
            await user.send(embed=message)

    async def send_embedded_message(
        self, user: int, title: str, description: str, link: str, thumbnail_url: str, footer: Optional[str] = None
    ) -> None:
        """
        Send an embedded message to a particular user
        """
        message = Embed.from_dict({
            "title": title,
            "description": description,
            "url": link,
            "color": DiscordBot.MESSAGE_EMBEDDED_COLOR,
            "thumbnail": {
                "url": thumbnail_url,
            },
            "footer": {
                "text": footer,
            },
        })
        await self.send_message(user, message)

    def _add_cogs(self, cog_classes: List[Type[Cog]]) -> None:
        for cog_class in cog_classes:
            self.add_cog(cog_class(self))

    def run(self):
        super().run(self._token)
