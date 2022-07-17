from mongoengine import Document, StringField, FloatField, LazyReferenceField

from core.db.time_logging_document import TimeLoggingDocument
from .manga import Manga


class MangaChapter(Document, TimeLoggingDocument):
    manga = LazyReferenceField(Manga, required=True)
    chapter = FloatField(min_value=0, required=True)
    link = StringField(max_length=255, required=True)
    site_name = StringField(max_length=255, required=True, choices=["MangaPark", "MangaFreak"])

    meta = {"collection": "manga_chapters"}
