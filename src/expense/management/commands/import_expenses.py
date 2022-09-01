import json
import re
from pathlib import Path
from typing import List

from django.conf import settings
from django.core.management.base import BaseCommand

from message.services.handlers import ExpenseMessageHandler


class Command(BaseCommand):
    help = "Import expense data."

    def handle(self, *args, **options):
        base_path = Path(__file__).parent
        content: List[str] = json.load(open(base_path / "expenses_messenger.json", "r"))
        user_id = settings.DISCORD_USER_ID

        for expense in content:
            ExpenseMessageHandler(expense, user_id, None, None).handle()
