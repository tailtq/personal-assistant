from rest_framework.request import Request

from core.views.base import BaseViewSet


class UIViewSet(BaseViewSet):
    def list(self, request: Request):
        return self.success("Hello World")
