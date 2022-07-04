from rest_framework import routers

from UI.views import UIViewSet

router = routers.SimpleRouter(trailing_slash=False)
router.register("", UIViewSet, basename="UI")

urlpatterns = router.urls
