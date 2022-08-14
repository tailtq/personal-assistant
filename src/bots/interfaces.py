from typing import Union, Optional

import discord


class BotInterface:
    async def send_message(self, user: int, message: Union[str, discord.Embed]) -> None:
        raise NotImplementedError()

    async def send_embedded_message(
        self,
        user: int,
        title: str,
        description: str,
        link: str,
        thumbnail_url: str,
        footer: Optional[str] = None
    ) -> None:
        raise NotImplementedError()
