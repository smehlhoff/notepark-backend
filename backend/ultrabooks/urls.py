from django.urls import path

from .views import CompanyListView, CompanyDetailView, UltrabooksListView, UltrabooksDetailView, \
    UltrabooksReleasedListView

app_name = 'ultrabooks'

urlpatterns = [
    path('ultrabooks/', UltrabooksListView.as_view()),
    path('ultrabooks/released/', UltrabooksReleasedListView.as_view()),
    path('ultrabooks/companies/', CompanyListView.as_view()),
    path('ultrabooks/companies/<slug>/', CompanyDetailView.as_view()),
    path('ultrabooks/<slug>/', UltrabooksDetailView.as_view()),
]
