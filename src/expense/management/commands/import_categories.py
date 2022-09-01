import json
import re
from pathlib import Path
from typing import List

from django.core.management.base import BaseCommand

from message.services.handlers import ExpenseMessageHandler


class Command(BaseCommand):
    help = "seed database for testing and development."

    def handle(self, *args, **options):
        base_path = Path(__file__).parent
        content: List[str] = json.load(open(base_path / "expenses_messenger.json", "r"))
        items = []

        for expense in content:
            # EXTRACT_EXPENSES_PATTERN
            expense = re.sub(ExpenseMessageHandler.EXTRACT_DATE_PATTERN, "", expense).strip()
            items += [item[0] for item in re.findall(ExpenseMessageHandler.EXTRACT_EXPENSES_PATTERN, expense)]

        items = [item.lower() for item in items]
        with open(base_path / "expense_items.json", "w") as f:
            json.dump(sorted(list(set(items))), f, indent=2)
        print(len(items), len(set(items)))
        # self.stdout.write("seeding data...")
        # run_seed(self, options['mode'])
        # self.stdout.write('done.')
