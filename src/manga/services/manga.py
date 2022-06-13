from typing import Type, List, Dict

from core.services.base import BaseService
from manga.models import Manga


class MangaService(BaseService):
    @property
    def model(self) -> Type[Manga]:
        return Manga

    def list_manga_with_latest_chapter(self) -> List[Dict]:
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
                    "name": 1,
                    "all_names": {"$concatArrays": [["$name"], "$other_names"]},
                    "latest_chapter": {"$ifNull": [{"$max": "$chapters.chapter"}, 0]}
                },
            }
        ]))
