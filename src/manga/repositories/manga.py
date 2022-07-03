from typing import Type, List, Dict

from mongoengine import Document

from core.repositories.base import BaseRepository
from manga.models import Manga


class MangaRepository(BaseRepository):
    @property
    def model(self) -> Type[Document]:
        return Manga

    def list_with_latest_chapter(self) -> List[Dict]:
        """
        Return manga list with the latest chapter
        """
        return list(self.model.objects.aggregate([
            {
                "$lookup": {
                    "from": "manga_chapters",
                    "localField": "_id",
                    "foreignField": "manga",
                    "as": "chapters"
                }
            },
            {
                "$project": {
                    "id": 1,
                    "name": 1,
                    "all_names": {"$concatArrays": [["$name"], "$other_names"]},
                    "latest_chapter": {"$ifNull": [{"$max": "$chapters.chapter"}, 0]}
                },
            }
        ]))
