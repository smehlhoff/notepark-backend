from django.urls import path

from .views import ReportView

app_name = 'reports'

urlpatterns = [
    path('reports/', ReportView.as_view()),
]
