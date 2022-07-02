from typing import List, Dict

from fuzzywuzzy import fuzz

from manga.dtos.manga import MangaChapterDTO
from manga.services import MangaService


class MangaFilter:
    def __init__(self):
        # TODO: fix the dependency here
        self._manga_service = MangaService()

    def filter(self, chapters: List[MangaChapterDTO]) -> List[MangaChapterDTO]:
        chapters = self._filter_duplicated_name_chapters(chapters)
        chapters = self._filter_unread_chapters(chapters)
        return chapters

    def _filter_unread_chapters(self, chapters: List[MangaChapterDTO]) -> List[MangaChapterDTO]:
        """
        1. Fetch all manga
        2. Use fuzzy search & chapter comparison to match each chapter with the respective manga
        3. Discard the non-interested manga chapters
        """
        new_chapters = []
        manga_list: List[Dict] = self._manga_service.list_manga_with_latest_chapter()

        for chapter in chapters:
            for manga in manga_list:
                for name in manga.get("all_names", []):
                    if all([
                        fuzz.ratio(name.lower(), chapter.manga_name.lower()) >= 90,
                        chapter.chapter > manga["latest_chapter"]
                    ]):
                        # formalize the name for the next step
                        chapter.manga_name = manga["name"]
                        chapter.manga_object_id = manga["_id"]
                        new_chapters.append(chapter)
                        break
                if chapter.manga_object_id:
                    break
        return new_chapters

    def _filter_duplicated_name_chapters(self, chapters: List[MangaChapterDTO]) -> List[MangaChapterDTO]:
        """
        Select the latest chapter for each manga after crawling
        """
        manga_name_index = {}

        for i, chapter in enumerate(chapters):
            if chapter.manga_name not in manga_name_index:
                manga_name_index[chapter.manga_name] = i
            elif chapters[manga_name_index[chapter.manga_name]].chapter < chapter.chapter:
                manga_name_index[chapter.manga_name] = i

        return [chapters[i] for i in manga_name_index.values()]
