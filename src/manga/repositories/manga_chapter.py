from typing import Type

from mongoengine import Document

from core.repositories.base import BaseRepository
from manga.models import MangaChapter


class MangaChapterRepository(BaseRepository):
    @property
    def model(self) -> Type[Document]:
        return MangaChapter
