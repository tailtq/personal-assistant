from typing import Type, List, Dict, Optional, Union

from bson import ObjectId
from fuzzywuzzy import fuzz

from core.services.base import BaseService
from manga.repositories.manga import MangaRepository


class MangaService(BaseService):
    def __init__(self):
        super().__init__(MangaRepository)
        self.repository: MangaRepository

    def list_with_latest_chapter(self) -> List[Dict]:
        return self.repository.list_with_latest_chapter()

    def check_manga_exist(self, name: str, _id: Optional[Union[str, int]] = None) -> bool:
        """
        Check manga exists in database
        """
        _id = _id if _id else ObjectId()
        mangas = self.repository.list(conditions={"pk__ne": _id}, fields=["name", "other_names"])
        fuzzy_scores = [
            fuzz.ratio(name.lower(), existed_name.lower())
            for manga in mangas
            for existed_name in manga.all_names
        ]
        return max(fuzzy_scores or [0]) > 90
    
    def _delete_relationships(self, _id: Union[str, int]):
        from manga.services import MangaChapterService

        MangaChapterService().delete(manga=_id)
