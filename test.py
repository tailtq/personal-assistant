from manga.services import MangaChapterService
from manga.services.manga import MangaService

manga_list = [
    {
         "name": 'One Piece',
         "thumbnailUrl": 'https://images.mangafreak.net/manga_images/one_piece.jpg',
         "otherNames": ([]),
    },
    {
        "name": 'Jagaaaaaan',
        "thumbnailUrl": 'https://cdn.truyentranh.net/upload/image/comic/20170303/jagaaaaaan-58b945b82d7bc-thumbnail-176x264.jpg',
        "otherNames": ([]),
        "chapters": [
            {
                "chapter": 12,
                "link": "abc",
            },
            {
                "chapter": 14,
                "link": "abc",
            }
        ]
    },
    {
        "name": 'Tokyo Revengers',
        "thumbnailUrl": 'https://images.mangafreak.net/manga_images/toukyou_revengers.jpg',
        "otherNames": ([
            'Tokyo卍Revengers',
            'Toukyou Revengers',
        ]),
        "chapters": [
            {
                "chapter": 13,
                "link": "abc",
            },
            {
                "chapter": 16,
                "link": "abc",
            }
        ]
    },
    {
        "name": 'My Hero Academia',
        "thumbnailUrl": 'https://xcdn-000.animemark.com/images/W600/02a/6044dcd1cc60840d83bdba20_223_350_62952.jpg',
        "otherNames": ([]),
    },
    {
        "name": 'Onepunch-Man',
        "thumbnailUrl": 'https://images.mangafreak.net/manga_images/onepunch_man.jpg',
        "otherNames": ([]),
    },
    {
        "name": 'Kanojo, Okarishimasu',
        "thumbnailUrl": 'https://images.mangafreak.net/manga_images/kanojo_okarishimasu.jpg',
        "otherNames": ([]),
    },
    {
        "name": 'How to Fight',
        "thumbnailUrl": 'https://xcdn-000.animemark.com/images/W600/ed6/60458203c9d6ca277900e6de_605_830_246998.png',
        "otherNames": ([]),
    },
]
manga_service = MangaService()
# print(list(manga_service.list_manga_with_latest_chapter()))
manga_chapter_service = MangaChapterService()

for manga in manga_list:
    manga_entity = manga_service.create(
        name=manga["name"], thumbnail_url=manga["thumbnailUrl"], other_names=manga["otherNames"],
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
