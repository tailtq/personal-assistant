import abc
import os
from enum import Enum

import requests
from pyppeteer import launch

from manga.const import MangaAccessMethod

EXEC_PATH = os.environ.get("GOOGLE_CHROME_SHIM", None)


class Crawler(abc.ABC):
    @abc.abstractmethod
    async def handle(self, url: str):
        pass

    @staticmethod
    def get_crawler(access_method: Enum):
        # Factory pattern (ɔ◔‿◔)ɔ ♥
        if access_method == MangaAccessMethod.HTTP_REQUESTS:
            return HTTPRequestCrawler()
        elif access_method == MangaAccessMethod.PUPPETEER:
            return PuppeteerCrawler()
        else:
            raise Exception()


class HTTPRequestCrawler(Crawler):
    async def handle(self, url: str) -> str:
        res = requests.get(url)
        res.encoding = "utf-8"
        return res.text


class PuppeteerCrawler(Crawler):
    async def handle(self, url: str) -> str:
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
