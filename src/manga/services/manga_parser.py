import re
import urllib.parse
from typing import List, Tuple

from bs4 import BeautifulSoup, Tag
import asyncio

from .crawlers import Crawler
from ..dtos.manga import MangaSiteDTO, MangaChapterDTO


class MangaParserService:
    def __init__(self, site: MangaSiteDTO):
        self._site = site
        # Bridge pattern (ɔ◔‿◔)ɔ ♥.
        # Instead of having 2-5 methods to crawl in this class, I separate them into individual classes to do crawling.
        self._crawler = Crawler.get_crawler(self._site.access_method)

    def parse_html(self) -> List[MangaChapterDTO]:
        """
        Crawl HTML content from site, parse the content to retrieve the newest manga
        """
        html = asyncio.run(self._crawler.handle(self._site.crawl_url))
        search_results = self._get_manga_list(html)
        manga: List[MangaChapterDTO] = []

        for result in search_results:
            # get manga name & link -> handle relative link
            manga_name = self._safe_get_html_element(result, self._site.manga_name)
            manga_chapter, manga_link = self._get_manga_latest_chapter(result)
            if manga_chapter is None or manga_link is None:
                continue
            manga_link = self._get_full_link(manga_link)
            manga.append(MangaChapterDTO(manga_name, manga_chapter, manga_link, self._site.lang, self._site.site_name))
        return manga

    @staticmethod
    def _safe_get_html_element(bs: Tag, tag: str, data_retrieved: str = "text") -> str:
        """
        Page 60: Web Scraping with Python
        """
        child_obj = bs.select(tag)
        if child_obj is not None and len(child_obj) > 0:
            if data_retrieved == "text":
                return child_obj[0].get_text().strip()
            elif "attr" in data_retrieved:
                data_retrieved = data_retrieved.split(":")[1]
                return child_obj[0].attrs[data_retrieved].strip()
        return ""

    def _get_manga_list(self, html: str) -> List[Tag]:
        """
        Get manga list
        """
        bs = BeautifulSoup(html, features="html.parser")
        if type(self._site.manga_list) == str:
            search_results: List[Tag] = bs.select(self._site.manga_list)
        else:
            search_results: List[Tag] = self._site.manga_list(bs)
        return search_results

    def _get_manga_latest_chapter(self, bs: Tag) -> Tuple[float, str]:
        """
        Get chapter number and chapter link using Regex. There are a few patterns we need to handle:
        - Chapter 45
        - Vol.0 Ch.3
        - Chapter 9: Story
        - Chapter 21.2
        - Vol.3 Chapter 36: French Onion Soup On A Rainy Day
        """
        result = (None, None)
        chapters = []
        chapter_tags: List[Tag] = bs.select(self._site.manga_chapter)
        if chapter_tags is not None and len(chapter_tags) > 0:
            for chapter_tag in chapter_tags:
                chapter = re.search(self._site.chapter_text_pattern, chapter_tag.get_text())
                if chapter:
                    chapter_number = float(chapter.groups()[-1])
                    link = chapter_tag.attrs["href"].strip()
                    chapters.append((chapter_number, link))
        if chapters:
            chapters = sorted(chapters, key=lambda x: x[0], reverse=True)
            result = chapters[0]
        return result

    def _get_full_link(self, link: str) -> str:
        """
        Get full link. For example
        From: /title/251351_resetting-lady/7462183_en_ch.25
        To: https://mangapark.net/title/251351_resetting-lady/7462183_en_ch.25
        """
        if not urllib.parse.urlparse(link).netloc:
            domain = urllib.parse.urlparse(self._site.crawl_url)
            domain = f"{domain.scheme}://{domain.netloc}/"
            link = link[1:] if link.startswith("/") else link
            link = f"{domain}{link}"
        return link
