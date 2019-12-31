from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Comment


def set_comment_public(modeladmin, request, queryset):
    rows_updated = queryset.update(public=True)

    if rows_updated == 1:
        modeladmin.message_user(request, 'Comment successfully set to public.')
    else:
        modeladmin.message_user(
            request, '{rows} comments successfully set to public.'.format(rows=rows_updated))


set_comment_public.short_description = 'Set public to selected comments'


def set_comment_private(modeladmin, request, queryset):
    rows_updated = queryset.update(public=False)

    if rows_updated == 1:
        modeladmin.message_user(
            request, 'Comment successfully set to private.')
    else:
        modeladmin.message_user(
            request, '{rows} comments successfully set to private.'.format(rows=rows_updated))


set_comment_private.short_description = 'Set private to selected comments'


def set_enable_comments(modeladmin, request, queryset):
    queryset.update(allow_comments=True)

    modeladmin.message_user(request, 'Posting comments is now enabled.')


set_enable_comments.short_description = 'Enable comment posting to selected objects'


def set_disable_comments(modeladmin, request, queryset):
    queryset.update(allow_comments=False)

    modeladmin.message_user(request, 'Posting comments is now disabled.')


set_disable_comments.short_description = 'Disable comment posting to selected objects'


def set_display_comments(modeladmin, request, queryset):
    queryset.update(display_comments=True)

    modeladmin.message_user(request, 'Comments will now be displayed.')


set_display_comments.short_description = 'Set display comments to selected objects'


def set_hide_comments(modeladmin, request, queryset):
    queryset.update(display_comments=False)

    modeladmin.message_user(request, 'Comments will now be hidden.')


set_hide_comments.short_description = 'Set hide comments to selected objects'


class CommentAdmin(admin.ModelAdmin):
    raw_id_fields = ('user',)
    list_display = ('id', 'user', 'public', 'content_type',
                    'object_link', 'report_count', 'created_at')
    search_fields = ('user', 'content')
    list_filter = ('public', 'created_at')
    fields = ('id', 'user', 'content', 'content_type', 'object_id', 'public', 'report_count', 'ip_address',
              'user_agent', 'created_at', 'updated_at')
    readonly_fields = ('id', 'object_link', 'report_count',
                       'ip_address', 'user_agent', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    actions = [set_comment_public, set_comment_private]

    def get_queryset(self, request):
        queryset = self.model._base_manager.get_queryset()
        ordering = self.get_ordering(request)

        if ordering:
            return queryset.order_by(*ordering)

        return queryset

    def get_actions(self, request):
        actions = super(CommentAdmin, self).get_actions(request)

        if not request.user.is_superuser and 'delete_selected' in actions:
            actions.pop('delete_selected')

        return actions

    def object_link(self, obj):
        content_type = obj.content_type

        url = reverse('admin:{app_label}_{model_name}_change'.format(
            app_label=content_type.app_label,
            model_name=content_type.model
        ), args=(obj.object_id,))

        return mark_safe('<a href="{url}">{id}</a>'.format(url=url, id=obj.object_id))


admin.site.register(Comment, CommentAdmin)
