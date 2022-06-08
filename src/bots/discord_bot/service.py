import time
from typing import Union

import discord
import asyncio

# from src.bots.base import BaseBot


class DiscordBot():
    MESSAGE_EMBEDDED_COLOR = "#0099ff"

    def __init__(self, token: str):
        self._token = token
        self._client = discord.Client(intents=discord.Intents(
            guilds=True,
            guild_messages=True,
            dm_messages=True,
        ))
        self._register_events()

    def _register_events(self):
        self._client.event(self.on_message)
        self._client.event(self.on_ready)

    async def on_message(self, message):
        if message.author == self._client.user:
            return
        # get intent -> handle relevant app
        # Note: All Discord messages must be sent via a channel (public, private)
        await message.channel.send("OK")
        await self.publish_message(480527832137728000, "Haha")

    async def on_ready(self):
        print("Discord Bot is ready")

    async def publish_message(self, user_id: int, message: Union[str, discord.Embed]) -> None:
        user: discord.User = await self._client.fetch_user(user_id)

        if type(message) == str:
            await user.dm_channel.send(content=message)
        elif type(message) == discord.Embed:
            await user.dm_channel.send(embed=message)
        # user = self._client.users.fetch(user_id)
        # self.client
        pass

    def publish_embedded_message(
        self, title: str, url: str, description: str, thumbnail: str, color=MESSAGE_EMBEDDED_COLOR
    ):
        """
        const embeddedMessage = new MessageEmbed()
            .setColor(this.MESSAGE_EMBEDDED_COLOR)
            .setTitle(title)
            .setURL(url)
            .setDescription(description)
            .setThumbnail(thumbnail)
            .setFooter(`From ${process.env.APP_ENVIRONMENT.toUpperCase()}`);
        const user = await this.client.users.fetch(userId);
        """
        embed = discord.Embed(title=title, url=url, description=description, thumbnail=thumbnail, color=color)

        pass

    # def run(self) -> None:
    #     asyncio.get_event_loop().run_until_complete(self._client.start(self._token))
        # await

    def run(self):
        self._client.run(self._token)


if __name__ == "__main__":
    bot = DiscordBot("ODg2NDI2OTQ5MjE0NDE2OTc2.YT1bbQ.bBT_CIQre0SQOszFY4yqlH_MenI")
    bot.run()
