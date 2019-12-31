from django.urls import path, re_path

from .views import NewsListView, LatestNewsDetailView, NewsDetailView

app_name = 'news'

urlpatterns = [
    path('news/', NewsListView.as_view()),
    path('news/latest/', LatestNewsDetailView.as_view()),
    re_path('news/(?P<slug>[\w/-]+)/', NewsDetailView.as_view()),
]
