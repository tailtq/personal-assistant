from ..const import MangaAccessMethod


class MangaSiteDTO:
    def __init__(
        self,
        site_name: str,
        lang: str,
        crawl_url: str,
        manga_list: str,
        manga_name: str,
        manga_chapter: str,
        manga_link: str,
        access_method: int = MangaAccessMethod.HTTP_REQUESTS,  # puppeteer, requests
    ):
        self.site_name = site_name
        self.lang = lang
        self.crawl_url = crawl_url
        self.manga_list = manga_list
        self.manga_name = manga_name
        self.manga_chapter = manga_chapter
        self.manga_link = manga_link
        self.access_method = access_method


class MangaChapterDTO:
    def __init__(self, manga_name: str, chapter: float, link: str, lang: str):
        self.manga_name = manga_name
        self.chapter = chapter
        self.link = link
        self.lang = lang
        self.manga_object_id = None

    def __repr__(self) -> str:
        return f"Manga: {self.manga_name}, chapter: {self.chapter}, link: {self.link}"
