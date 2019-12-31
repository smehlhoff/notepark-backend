from django.urls import path

from .views import FavoriteView, FavoriteRetrieveDeleteView

app_name = 'favorites'

urlpatterns = [
    path('favorites/', FavoriteView.as_view()),
    path('favorites/<object_id>/', FavoriteRetrieveDeleteView.as_view()),
]
