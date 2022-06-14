from typing import Type, List, Union

from bson import ObjectId

from core.services.base import BaseService
from ..dtos.manga import MangaChapterDTO
from ..models import MangaChapter


class MangaChapterService(BaseService):
    @property
    def model(self) -> Type[MangaChapter]:
        return MangaChapter

    def create_batch(
        self, chapters: List[MangaChapterDTO], load_bulk: bool = False,
    ) -> List[Union[ObjectId, MangaChapter]]:
        """
        Create a batch of entities
        """
        if len(chapters) == 0:
            return []
        chapters = [
            MangaChapter(manga=chapter.manga_object_id, chapter=chapter.chapter, link=chapter.link)
            for chapter in chapters
        ]
        return self.model.objects.insert(chapters, load_bulk=load_bulk)
