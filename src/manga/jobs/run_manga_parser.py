import json
from typing import List, Dict

from fuzzywuzzy import fuzz

from core.message_queue import RedisMessageQueueService
from manga.const import QueueMessage
from manga.dtos.manga import MangaChapterDTO, MangaSiteDTO
from manga.services import MangaChapterService
from manga.services.manga import MangaService
from manga.services.manga_parser import MangaParserService

CRAWLING_MANGA_SITES = [
    MangaSiteDTO(
        site_name="truyentranhtuan",
        lang="vi",
        crawl_url="http://truyentranhtuan.com/",
        manga_list="#story-list .manga-focus",
        manga_name=".manga a",
        manga_chapter=".chapter a",
        manga_link=".chapter a",
    ),
    MangaSiteDTO(
        site_name="mangapark",
        lang="en",
        crawl_url="https://mangapark.net/",
        manga_list="#release-list > .item",
        manga_name="a.fw-bold",
        manga_chapter="a.visited",
        manga_link="a.visited",
    ),
]


def _filter_not_reading_chapters(chapters: List[MangaChapterDTO]) -> List[MangaChapterDTO]:
    """
    1. Fetch all manga
    2. Use fuzzy search & chapter comparison to match each chapter with the respective manga
    3. Discard the non-interested manga chapters
    """
    new_chapters = []
    manga_list: List[Dict] = MangaService().list_manga_with_latest_chapter()

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


def _filter_manga_chapters_having_same_name(chapters: List[MangaChapterDTO]) -> List[MangaChapterDTO]:
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


def run_manga_parser() -> None:
    """

    """
    chapters: List[MangaChapterDTO] = []

    for manga_site in CRAWLING_MANGA_SITES:
        parser = MangaParserService(manga_site)
        chapters.extend(parser.parse_html())

    chapters = _filter_not_reading_chapters(chapters)
    chapters = _filter_manga_chapters_having_same_name(chapters)
    new_chapter_ids = MangaChapterService().create_batch(chapters)

    if new_chapter_ids:
        message_queue = RedisMessageQueueService("bots_message_queue")
        message_queue.push(json.dumps({
            "message": QueueMessage.MANGA_RELEASE,
            "data": {
                "chapter_ids": [str(chapter_id) for chapter_id in new_chapter_ids],
            },
        }))


run_manga_parser()
