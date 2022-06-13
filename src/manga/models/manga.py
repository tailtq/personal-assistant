from mongoengine import Document, StringField, ListField

from core.db.time_logging_document import TimeLoggingDocument


class Manga(Document, TimeLoggingDocument):
    name = StringField(max_length=255, required=True, unique=True)
    thumbnail_url = StringField(max_length=255, required=True)
    other_names = ListField(StringField(max_length=255), default=[])
