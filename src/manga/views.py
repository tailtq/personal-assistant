from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from manga.models.manga import Manga


class MangaList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        manga = Manga.objects.create(name="One Piece", thumbnail_url="https://images.mangafreak.net/manga_images/one_piece.jpg")
        return Response(manga, status=status.HTTP_200_OK)
