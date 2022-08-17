from mongoengine import StringField, BooleanField, DictField
from mongoengine.document import Document

from core.db.time_logging_document import TimeLoggingDocument
from message.const import AppName


class Message(Document, TimeLoggingDocument):
    user_id = StringField(max_length=20, required=True)
    app_name = StringField(max_length=255, required=True, choices=[
        AppName.REPORT,
        AppName.EXPENSE,
        AppName.UNCATEGORIZED,
    ])
    is_trained = BooleanField(default=False)
    human_text = StringField(required=True)
    bot_text = StringField(required=True)
    nlu_result = DictField()
    context = DictField()

    meta = {"collection": "messages"}
