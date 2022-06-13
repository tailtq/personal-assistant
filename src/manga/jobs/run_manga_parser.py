from typing import List, Dict

from fuzzywuzzy import fuzz

from manga.dtos.manga import MangaChapterDTO, MangaSiteDTO
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


def filter_not_reading_chapters(chapters: List[MangaChapterDTO], manga_list: List[Dict]) -> List[MangaChapterDTO]:
    new_chapters = []
    # using fuzzy search to match chapters & manga list saved into database
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


def filter_manga_chapters_having_same_name(chapters: List[MangaChapterDTO]) -> List[MangaChapterDTO]:
    manga_name_index = {}

    for i, chapter in enumerate(chapters):
        if chapter.manga_name not in manga_name_index:
            manga_name_index[chapter.manga_name] = i
        elif chapters[manga_name_index[chapter.manga_name]].chapter < chapter.chapter:
            manga_name_index[chapter.manga_name] = i

    return [chapters[i] for i in manga_name_index.values()]


def run_manga_parser() -> None:
    chapters: List[MangaChapterDTO] = [MangaChapterDTO("One Piece", 1010, "abc", "en")]
    manga_list: List[Dict] = MangaService().list_manga_with_latest_chapter()

    for manga_site in CRAWLING_MANGA_SITES:
        parser = MangaParserService(manga_site)
        chapters.extend(parser.parse_html())

    chapters = filter_not_reading_chapters(chapters, manga_list)
    # chapters = filter_manga_chapters_having_same_name(chapters)
    print(chapters)


run_manga_parser()
