from mongoengine import Document, LazyReferenceField, DecimalField, StringField, DateField

from core.db.time_logging_document import TimeLoggingDocument
from .expense_category import ExpenseCategory


class Expense(Document, TimeLoggingDocument):
    category = LazyReferenceField(ExpenseCategory, required=True)
    description = StringField(max_length=255)
    amount = DecimalField(required=True, min_value=0)
    currency = StringField(required=True, max_length=5, choices=["KVND", "$"])
    spent_at = DateField(required=True)

    meta = {"collection": "expenses"}
