import re
import time
import urllib.parse
from typing import List

import requests

from bs4 import BeautifulSoup, Tag

from ..const import MangaAccessMethod
from ..dtos.manga import MangaSiteDTO, MangaChapterDTO


class MangaParserService:
    def __init__(self, site: MangaSiteDTO):
        self._site = site

    @staticmethod
    def _crawl_html_content_by_http_requests(url: str) -> str:
        """
        Get raw HTML of a page using standard HTTP requests
        """
        res = requests.get(url)
        res.encoding = "utf-8"
        return res.text

    @staticmethod
    def _crawl_html_content_by_puppeteer(url: str) -> str:
        """
        Get raw HTML of a page using Puppeteer
        """
        pass

    def parse_html(self) -> List[MangaChapterDTO]:
        """
        Crawl HTML content from site, parse the content to retrieve the newest manga
        """
        html = ""
        if self._site.access_method == MangaAccessMethod.HTTP_REQUESTS:
            html = self._crawl_html_content_by_http_requests(self._site.crawl_url)
        elif self._site.access_method == MangaAccessMethod.PUPPETEER:
            html = self._crawl_html_content_by_puppeteer(self._site.crawl_url)

        bs = BeautifulSoup(html, features="html.parser")
        search_results: List[Tag] = bs.select(self._site.manga_list)
        manga: List[MangaChapterDTO] = []

        for result in search_results:
            manga_name = self._safe_get_html_element(result, self._site.manga_name)
            manga_link = self._safe_get_html_element(result, self._site.manga_link, data_retrieved="attr:href")
            if not urllib.parse.urlparse(manga_link).netloc:
                domain = urllib.parse.urlparse(self._site.crawl_url)
                domain = f"{domain.scheme}://{domain.netloc}/"
                manga_link = manga_link[1:] if manga_link.startswith("/") else manga_link
                manga_link = domain + manga_link

            manga_chapter = re.search("[\d.]+", self._safe_get_html_element(result, self._site.manga_chapter))
            manga_chapter = float(manga_chapter.group(0)) if manga_chapter else 0
            manga.append(MangaChapterDTO(manga_name, manga_chapter, manga_link, self._site.lang))
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
