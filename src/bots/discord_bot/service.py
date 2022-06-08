from typing import Union

import discord

from bots.base import BaseBot


class DiscordBot(BaseBot):
    MESSAGE_EMBEDDED_COLOR = "#0099ff"

    def __init__(self, token: str):
        super().__init__(token)
        self._client = discord.Client(intents=discord.Intents(guilds=True, guild_messages=True, dm_messages=True))
        self._register_events()

    def _register_events(self):
        self._client.event(self.on_message)
        self._client.event(self.on_ready)
        self._client.event(self.on_error)

    async def on_message(self, message: discord.Message):
        if message.author == self._client.user:
            return
        # message.content == 'raise-exception'
        # get intent -> handle relevant app
        # Note: All Discord messages must be sent via a channel (public, private)
        await message.channel.send("OK")
        await self.send_message(480527832137728000, "Haha")

    async def on_ready(self):
        print(f"{self._client.user} is ready!")

    async def on_error(self, event, *args, **kwargs):
        raise

    async def send_message(self, user: Union[int, discord.User], message: Union[str, discord.Embed]) -> None:
        """
        Send message to a particular user
        """
        user: discord.User = await self._client.fetch_user(user) if type(user) == int else user

        if type(message) == str:
            await user.dm_channel.send(content=message)
        elif type(message) == discord.Embed:
            await user.dm_channel.send(embed=message)

    async def send_embed_message(self, user_id: int, embed: discord.Embed):
        """
        Send embed message to a particular user
        """
        # embed = discord.Embed(title=title, url=url, description=description, thumbnail=thumbnail, color=color)
        await self.send_message(user_id, embed)

    def run(self):
        self._client.run(self._token)


if __name__ == "__main__":
    # to run this, initialize the bot in main thread, run it in another one
    bot = DiscordBot("ODg2NDI2OTQ5MjE0NDE2OTc2.YT1bbQ.bBT_CIQre0SQOszFY4yqlH_MenI")
    bot.run()
