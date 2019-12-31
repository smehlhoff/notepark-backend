from django.contrib import admin

from backend.comments.admin import set_enable_comments, set_disable_comments, set_display_comments, set_hide_comments
from .models import News


def set_news_public(modeladmin, request, queryset):
    rows_updated = queryset.update(public=True)

    if rows_updated == 1:
        modeladmin.message_user(
            request, 'News article successfully set to public.')
    else:
        modeladmin.message_user(
            request, '{rows} news articles successfully set to public.'.format(rows=rows_updated))


set_news_public.short_description = 'Set public to selected news articles'


def set_news_private(modeladmin, request, queryset):
    rows_updated = queryset.update(public=False)

    if rows_updated == 1:
        modeladmin.message_user(
            request, 'News article successfully set to private.')
    else:
        modeladmin.message_user(
            request, '{rows} news articles successfully set to private.'.format(rows=rows_updated))


set_news_private.short_description = 'Set private to selected news articles'


class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'public', 'allow_comments',
                    'display_comments', 'comment_count', 'created_at')
    search_fields = ('title', 'content')
    list_filter = ('status', 'public', 'created_at')
    fields = ('id', 'title', 'slug', 'content', 'status', 'public', 'allow_comments', 'display_comments',
              'comment_count', 'created_at', 'updated_at')
    readonly_fields = ('id', 'slug', 'comment_count',
                       'created_at', 'updated_at')
    ordering = ('-created_at',)
    actions = [set_news_public, set_news_private, set_enable_comments, set_disable_comments, set_display_comments,
               set_hide_comments]

    def get_queryset(self, request):
        queryset = self.model._base_manager.get_queryset()
        ordering = self.get_ordering(request)

        if ordering:
            return queryset.order_by(*ordering)

        return queryset

    def get_actions(self, request):
        actions = super(NewsAdmin, self).get_actions(request)

        if not request.user.is_superuser and 'delete_selected' in actions:
            actions.pop('delete_selected')

        return actions


admin.site.register(News, NewsAdmin)
