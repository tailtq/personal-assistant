from mongoengine import Document, StringField, FloatField, LazyReferenceField

from core.db.time_logging_document import TimeLoggingDocument
from .manga import Manga


class MangaChapter(Document, TimeLoggingDocument):
    manga = LazyReferenceField(Manga, required=True)
    name = StringField(max_length=255)
    number = FloatField(min_value=0, required=True)
    link = StringField(max_length=255, required=True)
