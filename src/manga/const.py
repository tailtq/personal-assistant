from enum import Enum


class MangaAccessMethod(Enum):
    HTTP_REQUESTS = 1
    PUPPETEER = 2


class QueueMessage:
    MANGA_RELEASE = "NEW_CHAPTER_RELEASE"
