from discord.ext import commands, tasks

from core.message_queue import RedisMessageQueueService


class RedisListenerCog(commands.Cog):
    def __init__(self, bot):
        self._bot = bot
        self.listen_to_redis.start()
        self._message_queue = RedisMessageQueueService("bots_message_queue")

    def cog_unload(self):
        self.listen_to_redis.cancel()

    @tasks.loop(seconds=1.0)
    async def listen_to_redis(self):
        while not self._message_queue.is_empty():
            message = self._message_queue.pull()
            print("OKE OKE OKE", message, type(message))
        print("Running listener")

    @listen_to_redis.before_loop
    async def before_printer(self):
        print('waiting...')
        await self._bot.wait_until_ready()
