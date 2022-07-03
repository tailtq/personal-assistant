from typing import Type, List, Union

from bson import ObjectId

from core.services.base import BaseService
from ..dtos.manga import MangaChapterDTO
from ..models import MangaChapter
from ..repositories.manga_chapter import MangaChapterRepository


class MangaChapterService(BaseService):
    def __init__(self):
        super().__init__(MangaChapterRepository)

    def create_batch(
        self, chapters: List[MangaChapterDTO], load_multiple: bool = False,
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
        return self.repository.create(chapters, load_multiple=load_multiple)

    def _delete_relationships(self, _id: Union[str, int]):
        pass
