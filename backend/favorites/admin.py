from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Favorite


def set_enable_favorites(modeladmin, request, queryset):
    queryset.update(allow_favorites=True)

    modeladmin.message_user(request, 'Saving favorites is now enabled.')


set_enable_favorites.short_description = 'Enable saving favorites to selected ultrabooks.'


def set_disable_favorites(modeladmin, request, queryset):
    queryset.update(allow_favorites=False)

    modeladmin.message_user(request, 'Saving favorites is now disabled.')


set_disable_favorites.short_description = 'Disable saving favorites to selected ultrabooks.'


def set_display_favorites(modeladmin, request, queryset):
    queryset.update(display_favorites=True)

    modeladmin.message_user(request, 'Favorites will now be displayed.')


set_display_favorites.short_description = 'Set display favorites to selected ultrabooks'


def set_hide_favorites(modeladmin, request, queryset):
    queryset.update(display_favorites=False)

    modeladmin.message_user(request, 'Favorites will now be hidden.')


set_hide_favorites.short_description = 'Set hide favorites to selected ultrabooks'


class FavoriteAdmin(admin.ModelAdmin):
    raw_id_fields = ('user',)
    list_display = ('id', 'user', 'content_type', 'object_link', 'created_at')
    search_fields = ('user',)
    list_filter = ('created_at',)
    fields = ('id', 'user', 'content_type',
              'object_id', 'created_at', 'updated_at')
    readonly_fields = ('id', 'object_link', 'created_at', 'updated_at')
    ordering = ('-created_at',)

    def get_queryset(self, request):
        queryset = self.model._base_manager.get_queryset()
        ordering = self.get_ordering(request)

        if ordering:
            return queryset.order_by(*ordering)

        return queryset

    def get_actions(self, request):
        actions = super(FavoriteAdmin, self).get_actions(request)

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


admin.site.register(Favorite, FavoriteAdmin)
