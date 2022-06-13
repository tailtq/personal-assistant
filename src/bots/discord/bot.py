from typing import Union, List, Type

import discord
from discord.ext.commands import Bot, Cog

from bots.base import BaseBot


class DiscordBot(BaseBot, Bot):
    MESSAGE_EMBEDDED_COLOR = "#0099ff"

    def __init__(self, token: str, cog_classes: List[Type[Cog]] = None):
        BaseBot.__init__(self, token, command_prefix="")
        self._add_cogs(cog_classes)

    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return
        # message.content == 'raise-exception'
        # get intent -> handle relevant app
        # Note: All Discord messages must be sent via a channel (public, private)
        await message.channel.send("OK")
        await self.send_message(480527832137728000, "Haha")

    async def on_ready(self):
        print(f"{self.user} is ready!")

    async def on_error(self, event, *args, **kwargs):
        raise

    async def send_message(self, user: Union[int, discord.User], message: Union[str, discord.Embed]) -> None:
        """
        Send message to a particular user
        """
        if type(user) == int:
            user = await self.fetch_user(user)

        if type(message) == str:
            await user.dm_channel.send(content=message)
        elif type(message) == discord.Embed:
            await user.dm_channel.send(embed=message)

    async def send_embed_message(self, user_id: int, embed: discord.Embed) -> None:
        """
        Send embed message to a particular user
        """
        await self.send_message(user_id, embed)

    def _add_cogs(self, cog_classes: List[Type[Cog]]) -> None:
        for cog_class in cog_classes:
            self.add_cog(cog_class(self))

    def run(self):
        super().run(self._token)
