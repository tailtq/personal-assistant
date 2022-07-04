from rest_framework.request import Request

from core.views.base import BaseViewSet
from manga.serializers.manga import MangaSerializer
from manga.services import MangaService


class MangaViewSet(BaseViewSet):
    serializer_class = MangaSerializer

    """
    List all snippets, or create a new snippet.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._service = MangaService()

    def list(self, request: Request):
        serializer = self.serializer_class(self._service.list(), many=True)
        return self.success(serializer.data)

    def create(self, request: Request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return self.success(serializer.data)
        return self.error(serializer.errors)

    def update(self, request: Request, pk: str):
        serializer = self.serializer_class(data=request.data, context={"_id": pk})
        if serializer.is_valid():
            serializer.save()
            return self.success(serializer.data)
        return self.error(serializer.errors)

    def delete(self, request: Request, pk: str):
        count = self._service.delete_by_id(pk)
        if count != 0:
            return self.success({"total": count})
        return self.error()
