from typing import List

from django.conf import settings

from manga.services import MangaChapterService
from ..bot import DiscordBotInterface


class MangaReleaseHandler:
    def __init__(self, bot: DiscordBotInterface, chapter_ids: List[str]):
        self._bot = bot
        self._chapter_ids = chapter_ids

    async def handle(self):
        user_id: int = settings.DISCORD_USER_ID
        chapters = MangaChapterService().list(id__in=self._chapter_ids)

        for chapter in chapters:
            manga = chapter.manga.fetch()
            chapter_number = chapter.chapter
            chapter_number = int(chapter_number) if chapter_number == int(chapter_number) else chapter_number

            title = f"Manga Release - {manga.name}"
            description = f"Chapter {chapter_number} has been released. Check it out."
            await self._bot.send_embedded_message(user_id, title, description, chapter.link, manga.thumbnail_url)
