from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/', include('backend.comments.urls', namespace='comments')),
    path('v1/', include('backend.favorites.urls', namespace='favorites')),
    path('v1/', include('backend.news.urls', namespace='news')),
    path('v1/', include('backend.reports.urls', namespace='reports')),
    path('v1/', include('backend.tickets.urls', namespace='tickets')),
    path('v1/', include('backend.ultrabooks.urls', namespace='ultrabooks')),
    path('v1/', include('backend.users.urls', namespace='users')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

admin.site.site_header = getattr(settings, 'ADMIN_SITE_HEADER')
admin.site.index_title = getattr(settings, 'ADMIN_SITE_INDEX_TITLE')
admin.site.site_title = getattr(settings, 'ADMIN_SITE_TITLE')
admin.site.site_url = getattr(settings, 'SITE_URL')


def page_not_found(request, exception):
    response = {
        'detail': 'Not found.'
    }

    return JsonResponse(response, status=404)


def server_error(request):
    response = {
        'detail': 'The server encountered an internal error.'
    }

    return JsonResponse(response, status=500)


handler404 = page_not_found
handler500 = server_error
