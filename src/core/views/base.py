from typing import Any

from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import status as http_status


class BaseViewSet(ViewSet):
    @staticmethod
    def success(data: Any = None, status: int = http_status.HTTP_200_OK) -> Response:
        response = {
            "ok": True,
            "data": data,
            "errors": None,
        }
        return Response(response, status=status)

    @staticmethod
    def error(errors: Any = None, status: int = http_status.HTTP_400_BAD_REQUEST) -> Response:
        response = {
            "ok": False,
            "data": None,
            "errors": errors,
        }
        return Response(response, status=status)
