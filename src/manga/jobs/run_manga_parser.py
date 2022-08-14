import json
from typing import List

# Configure sentry
import sentry_sdk.utils

from core.config.sentry import *
from core.services import RedisMessageQueueService
from manga.const import QueueMessage, MangaAccessMethod
from manga.dtos.manga import MangaChapterDTO, MangaSiteDTO
from manga.services import MangaChapterService
from manga.services.manga_filter import MangaFilter
from manga.services.manga_parser import MangaParserService

CRAWLING_MANGA_SITES = [
    # MangaSiteDTO(
    #     site_name="truyentranhtuan",
    #     lang="vi",
    #     crawl_url="http://truyentranhtuan.com/",
    #     manga_list="#story-list .manga-focus",
    #     manga_name=".manga a",
    #     manga_chapter=".chapter a",
    # ),
    MangaSiteDTO(
        site_name="MangaFreak",
        lang="en",
        crawl_url="https://w13.mangafreak.net/",
        manga_list=".latest_list:first-child > .latest_item",
        manga_name="a.name",
        chapter_text_pattern=r"Chapter ([0-9.]+)",
        manga_chapter=".chapter_box a:first-child",
    ),
    MangaSiteDTO(
        site_name="MangaPark",
        lang="en",
        crawl_url="https://mangapark.net/",
        manga_list="#latest_release .group",
        manga_name="h3.text-lg a",
        manga_chapter="ul li a",
        chapter_text_pattern=r"(Chapter |Ch\.)([0-9.]+)",
        access_method=MangaAccessMethod.PUPPETEER,
    ),
]


def run_manga_parser() -> None:
    """
    Run manga parser
    """
    sentry_sdk.capture_message("Scheduler is running")

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
