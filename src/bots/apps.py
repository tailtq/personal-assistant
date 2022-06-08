import threading

from django.apps import AppConfig

from bots.discord_bot.service import DiscordBot


class BotsConfig(AppConfig):
    name = 'bots'

    def ready(self):
        print("Create a new thread here")
        # TODO: Continue this one
        # thread = threading.Thread(target=self.run_bots, daemon=True)
        # print("Main thread:", threading.get_ident())
        # thread.start()

    def run_bots(self):
        print("Sub-thread:", threading.get_ident())

        bot: DiscordBot
        bot = DiscordBot.get_bot("ODg2NDI2OTQ5MjE0NDE2OTc2.YT1bbQ.bBT_CIQre0SQOszFY4yqlH_MenI")
        bot.run()
