import json
from typing import List

from core.message_queue import RedisMessageQueueService
from manga.const import QueueMessage
from manga.dtos.manga import MangaChapterDTO, MangaSiteDTO
from manga.services import MangaChapterService
from manga.services.manga_filter import MangaFilter
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


def run_manga_parser() -> None:
    """
    Run manga parser
    """
    try:
        chapters: List[MangaChapterDTO] = []

        for manga_site in CRAWLING_MANGA_SITES:
            parser = MangaParserService(manga_site)
            chapters.extend(parser.parse_html())

        chapters = MangaFilter().filter(chapters)
        new_chapter_ids = MangaChapterService().create_batch(chapters)

        if new_chapter_ids:
            message_queue = RedisMessageQueueService("bots_message_queue")
            message_queue.push(json.dumps({
                "message": QueueMessage.MANGA_RELEASE,
                "data": {
                    "chapter_ids": [str(chapter_id) for chapter_id in new_chapter_ids],
                },
            }))
    except Exception as e:
        # TODO: Log to sentry
        print(e)


run_manga_parser()
