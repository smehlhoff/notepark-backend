from django.urls import path

from .views import CommentView

app_name = 'comments'

urlpatterns = [
    path('comments/', CommentView.as_view()),
]
