import json
import re
from pathlib import Path
from typing import List

from django.core.management.base import BaseCommand

from message.services import ExpenseMessageHandler


class Command(BaseCommand):
    help = "seed database for testing and development."

    def handle(self, *args, **options):
        content: List[str] = json.load(open(Path(__file__).parent / "expenses_messenger.json", "r"))
        items = []

        for expense in content:
            # EXTRACT_EXPENSES_PATTERN
            expense = re.sub(ExpenseMessageHandler.EXTRACT_DATE_PATTERN, "", expense).strip()
            items += [item[0] for item in re.findall(ExpenseMessageHandler.EXTRACT_EXPENSES_PATTERN, expense)]
        print(len(items), len(set(items)), set(items))
        # self.stdout.write("seeding data...")
        # run_seed(self, options['mode'])
        # self.stdout.write('done.')
