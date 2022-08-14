from django.core.management.base import BaseCommand
from django.conf import settings

from bots.discord.bot import DiscordBot
from bots.discord.cogs.redis_listener import RedisListenerCog


class Command(BaseCommand):
    help = "Run a discord bot"

    def handle(self, *args, **kwargs):
        if not settings.DISCORD_TOKEN:
            raise Exception("Discord Token not found")
        bot: DiscordBot = DiscordBot.get_bot(settings.DISCORD_TOKEN, [RedisListenerCog])
        bot.run()
