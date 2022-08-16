from mongoengine import StringField, BooleanField, EmbeddedDocumentField, DictField
from mongoengine.document import Document

from core.db.time_logging_document import TimeLoggingDocument
from message.const import AppName


class Message(Document, TimeLoggingDocument):
    app_name = StringField(max_length=255, required=True, choices=[
        AppName.REPORT,
        AppName.EXPENSE,
        AppName.UNCATEGORIZED,
    ])
    is_trained = BooleanField(default=False)
    human_text = StringField(required=True)
    bot_text = StringField(required=True)
    nlu_result = DictField()

    meta = {"collection": "messages"}
