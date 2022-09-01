import json

from discord.ext import commands, tasks

from core.services import RedisMessageQueueService
from manga.const import QueueMessage
from bots.discord.bot import DiscordBot
from bots.discord.handlers.manga_release import MangaReleaseHandler


class RedisListenerCog(commands.Cog):
    def __init__(self, bot: DiscordBot):
        self._bot = bot
        self.listen_to_redis.start()
        self._message_queue = RedisMessageQueueService("bots_message_queue")

    def cog_unload(self):
        self.listen_to_redis.cancel()

    @tasks.loop(seconds=1.0)
    async def listen_to_redis(self):
        while not self._message_queue.is_empty():
            message: bytes = self._message_queue.pull()
            message: dict = json.loads(message.decode("utf-8"))

            if message["message"] == QueueMessage.MANGA_RELEASE:
                await MangaReleaseHandler(self._bot, **message["data"]).handle()

    @listen_to_redis.before_loop
    async def before_printer(self):
        print('waiting...')
        await self._bot.wait_until_ready()
