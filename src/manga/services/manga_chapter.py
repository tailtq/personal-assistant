from typing import Type

from core.services.base import BaseService
from manga.models import MangaChapter


class MangaChapterService(BaseService):
    @property
    def model(self) -> Type[MangaChapter]:
        return MangaChapter
