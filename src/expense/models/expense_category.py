from mongoengine import Document, LazyReferenceField, StringField, ListField

from core.db.time_logging_document import TimeLoggingDocument


class ExpenseCategory(Document, TimeLoggingDocument):
    parent = LazyReferenceField("ExpenseCategory")
    title = StringField(max_length=255, required=True)
    description = StringField(max_length=255)
    icon_url = StringField(max_length=255)
    items = ListField(StringField(max_length=255), default=[])

    meta = {"collection": "expense_categories"}
