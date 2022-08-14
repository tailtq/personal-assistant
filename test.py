from datetime import datetime, date
from expense.services import ExpenseMessageHandler

handler = ExpenseMessageHandler("13/8 breakfast 50k (I need to do something), vision 25k", None)
print("handler.is_valid()", handler.is_valid())
print("handler.handle()", handler.handle())

# spent_at = datetime.strptime(f"30/4/{date.today().year}", "%d/%m/%Y")
# print(spent_at)
# spent_at.
# date.s
