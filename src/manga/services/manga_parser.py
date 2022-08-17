import os
import re
import urllib.parse
from typing import List, Tuple

import requests

from bs4 import BeautifulSoup, Tag
from pyppeteer import launch
import asyncio

from ..const import MangaAccessMethod
from ..dtos.manga import MangaSiteDTO, MangaChapterDTO

EXEC_PATH = os.environ.get("GOOGLE_CHROME_SHIM", None)


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
    async def _crawl_html_content_by_puppeteer(url: str) -> str:
        """
        Get raw HTML of a page using Puppeteer
        """
        browser = await launch(headless=True, executablePath=EXEC_PATH, args=[
            "--no-sandbox",
            "--single-process",
            "--disable-dev-shm-usage",
            "--disable-gpu",
            "--no-zygote",
        ])
        page = await browser.newPage()
        await page.goto(url)
        await page.waitFor(1.5)
        content = await page.content()
        await browser.close()

        return content

    def parse_html(self) -> List[MangaChapterDTO]:
        """
        Crawl HTML content from site, parse the content to retrieve the newest manga
        """
        html = ""
        if self._site.access_method == MangaAccessMethod.HTTP_REQUESTS:
            html = self._crawl_html_content_by_http_requests(self._site.crawl_url)
        elif self._site.access_method == MangaAccessMethod.PUPPETEER:
            html = asyncio.run(self._crawl_html_content_by_puppeteer(self._site.crawl_url))

        bs = BeautifulSoup(html, features="html.parser")
        search_results: List[Tag] = bs.select(self._site.manga_list)
        manga: List[MangaChapterDTO] = []

        for result in search_results:
            # get manga name & link -> handle relative link
            manga_name = self._safe_get_html_element(result, self._site.manga_name)
            manga_chapter, manga_link = self._get_manga_latest_chapter(
                result, self._site.manga_chapter, self._site.chapter_text_pattern
            )
            if manga_chapter is None or manga_link is None:
                continue
            if not urllib.parse.urlparse(manga_link).netloc:
                domain = urllib.parse.urlparse(self._site.crawl_url)
                domain = f"{domain.scheme}://{domain.netloc}/"
                manga_link = manga_link[1:] if manga_link.startswith("/") else manga_link
                manga_link = domain + manga_link
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

    @staticmethod
    def _get_manga_latest_chapter(bs: Tag, tag: str, chapter_text_pattern: str) -> Tuple[float, str]:
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
        child_objs: List[Tag] = bs.select(tag)
        if child_objs is not None and len(child_objs) > 0:
            for obj in child_objs:
                chapter_number = float(re.search(chapter_text_pattern, obj.get_text()).groups()[-1])
                link = obj.attrs["href"].strip()
                chapters.append((chapter_number, link))
        if chapters:
            chapters = sorted(chapters, key=lambda x: x[0], reverse=True)
            result = chapters[0]
        return result
