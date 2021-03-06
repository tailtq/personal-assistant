from rest_framework import routers

from manga.views import MangaViewSet

router = routers.SimpleRouter(trailing_slash=False)
router.register("", MangaViewSet, basename="Manga")

urlpatterns = router.urls
