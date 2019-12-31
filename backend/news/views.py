from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import News
from .pagination import NewsPagination
from .serializers import NewsSerializer, NewsDetailSerializer


class NewsListView(generics.ListAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = (AllowAny,)
    pagination_class = NewsPagination


class LatestNewsDetailView(generics.RetrieveAPIView):
    serializer_class = NewsDetailSerializer
    permission_classes = (AllowAny,)

    def get_object(self):
        try:
            queryset = News.objects.latest('created_at').id
        except News.DoesNotExist:
            queryset = None

        obj = get_object_or_404(News, id=queryset)

        return obj


class NewsDetailView(generics.RetrieveAPIView):
    queryset = News.objects.all()
    serializer_class = NewsDetailSerializer
    lookup_field = 'slug'
    permission_classes = (AllowAny,)
