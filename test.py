from manga.services import MangaChapterService
from manga.services.manga import MangaService

manga_list = [
    {
         "name": "One Piece",
         "thumbnail_url": "https://images.mangafreak.net/manga_images/one_piece.jpg",
    },
    {
        "name": "Jagaaaaaan",
        "thumbnail_url": "https://cdn.truyentranh.net/upload/image/comic/20170303/jagaaaaaan-58b945b82d7bc-thumbnail-176x264.jpg"
    },
    {
        "name": "Tokyo Revengers",
        "thumbnail_url": "https://images.mangafreak.net/manga_images/toukyou_revengers.jpg",
        "other_names": [
            "Tokyo卍Revengers",
            "Toukyou Revengers",
        ]
    },
    {
        "name": "My Hero Academia",
        "thumbnail_url": "https://xcdn-000.animemark.com/images/W600/02a/6044dcd1cc60840d83bdba20_223_350_62952.jpg"
    },
    {
        "name": "Onepunch-Man",
        "thumbnail_url": "https://images.mangafreak.net/manga_images/onepunch_man.jpg"
    },
    {
        "name": "Kanojo, Okarishimasu",
        "thumbnail_url": "https://images.mangafreak.net/manga_images/kanojo_okarishimasu.jpg"
    },
    {
        "name": "How to Fight",
        "thumbnail_url": "https://xcdn-000.animemark.com/images/W600/ed6/60458203c9d6ca277900e6de_605_830_246998.png"
    },
]
manga_service = MangaService()
# print(list(manga_service.list_with_latest_chapter()))
manga_chapter_service = MangaChapterService()

for manga in manga_list:
    manga_entity = manga_service.create(
        name=manga["name"], thumbnail_url=manga["thumbnail_url"], other_names=manga["other_names"],
    )
    chapters = manga.get("chapters", [])

    for chapter in chapters:
        print(manga_chapter_service.create(manga=manga_entity, **chapter))

# manga_site = MangaSiteDTO(
#     site_"name"="mangapark",
#     lang="en",
#     crawl_url="https://mangapark.net/",
#     manga_list="#release-list > .item",
#     manga_"name"="a.fw-bold",
#     manga_chapter="a.visited",
#     manga_link="a.visited",
# )
# parser = MangaParserService(manga_site)
# results = parser.parse_html()
