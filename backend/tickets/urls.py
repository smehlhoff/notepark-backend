from django.urls import path

from .views import TicketView

app_name = 'tickets'

urlpatterns = [
    path('contact/', TicketView.as_view()),
]
