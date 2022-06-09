from django.core.management.base import BaseCommand
from django.conf import settings

from bots.discord.service import DiscordBot


class Command(BaseCommand):
    help = "Run a discord bot"

    def handle(self, *args, **options):
        bot: DiscordBot
        bot = DiscordBot.get_bot("ODg2NDI2OTQ5MjE0NDE2OTc2.YT1bbQ.bBT_CIQre0SQOszFY4yqlH_MenI")
        # TODO: add redis event listener

        bot.run()
