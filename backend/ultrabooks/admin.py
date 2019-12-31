from django.contrib import admin

from backend.comments.admin import set_enable_comments, set_disable_comments, set_display_comments, set_hide_comments
from backend.favorites.admin import set_enable_favorites, set_disable_favorites, set_display_favorites, \
    set_hide_favorites
from .models import Company, Color, Processor, VideoCard, Memory, Storage, OperatingSystem, Image, Ultrabooks


class CategoryBaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    fields = ('id', 'name', 'created_at', 'updated_at')
    readonly_fields = ('id', 'created_at', 'updated_at')
    ordering = ('name',)


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at', 'updated_at')
    fields = ('id', 'name', 'slug', 'created_at', 'updated_at')
    readonly_fields = ('id', 'slug', 'created_at', 'updated_at')
    ordering = ('name',)


class ColorAdmin(admin.ModelAdmin):
    list_display = ('color', 'created_at', 'updated_at')
    fields = ('id', 'color', 'created_at', 'updated_at')
    readonly_fields = ('id', 'created_at', 'updated_at')
    ordering = ('color',)


class MemoryAdmin(admin.ModelAdmin):
    list_display = ('speed', 'created_at', 'updated_at')
    fields = ('id', 'speed', 'created_at', 'updated_at')
    readonly_fields = ('id', 'created_at', 'updated_at')
    ordering = ('speed',)


class StorageAdmin(admin.ModelAdmin):
    list_display = ('capacity', 'created_at', 'updated_at')
    fields = ('id', 'capacity', 'created_at', 'updated_at')
    readonly_fields = ('id', 'created_at', 'updated_at')
    ordering = ('capacity',)


class ImageAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at', 'updated_at')
    fields = ('id', 'name', 'slug', 'created_at', 'updated_at')
    readonly_fields = ('id', 'created_at', 'updated_at')
    ordering = ('name',)


def set_ultrabooks_public(modeladmin, request, queryset):
    rows_updated = queryset.update(public=True)

    if rows_updated == 1:
        modeladmin.message_user(
            request, 'Ultrabook successfully set to public.')
    else:
        modeladmin.message_user(
            request, '{rows} ultrabooks successfully set to public.'.format(rows=rows_updated))


set_ultrabooks_public.short_description = 'Set public to selected ultrabooks'


def set_ultrabooks_private(modeladmin, request, queryset):
    rows_updated = queryset.update(public=False)

    if rows_updated == 1:
        modeladmin.message_user(
            request, 'Ultrabook successfully set to private.')
    else:
        modeladmin.message_user(
            request, '{rows} ultrabooks successfully set to private.'.format(rows=rows_updated))


set_ultrabooks_private.short_description = 'Set private to selected ultrabooks'


class UltrabooksAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'public', 'allow_comments', 'display_comments', 'comment_count',
                    'allow_favorites', 'display_favorites', 'favorite_count', 'created_at')
    search_fields = ('name',)
    list_filter = ('name', 'status', 'public', 'created_at')
    fields = ('id', 'name', 'slug', 'company', 'launch_date', 'weight', 'dimensions', 'design_colors',
              'processor_models', 'video_card_models', 'memory_models', 'storage_models', 'display_size',
              'display_resolution', 'battery', 'wireless', 'video', 'audio', 'connectivity', 'operating_system_models',
              'optical_drive', 'features', 'images', 'status', 'public', 'allow_comments', 'display_comments',
              'comment_count', 'allow_favorites', 'display_favorites', 'favorite_count', 'created_at', 'updated_at')
    readonly_fields = ('id', 'slug', 'comment_count',
                       'favorite_count', 'created_at', 'updated_at')
    filter_horizontal = ('design_colors', 'processor_models', 'video_card_models', 'memory_models', 'storage_models',
                         'operating_system_models', 'images')
    save_on_top = True
    ordering = ('-created_at',)
    actions = [set_enable_favorites, set_disable_favorites, set_display_favorites, set_hide_favorites,
               set_enable_comments, set_disable_comments, set_display_comments, set_hide_comments]

    def get_queryset(self, request):
        queryset = self.model._base_manager.get_queryset()
        ordering = self.get_ordering(request)

        if ordering:
            return queryset.order_by(*ordering)

        return queryset

    def get_actions(self, request):
        actions = super(UltrabooksAdmin, self).get_actions(request)

        if not request.user.is_superuser and 'delete_selected' in actions:
            actions.pop('delete_selected')

        return actions


admin.site.register(Company, CompanyAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Processor, CategoryBaseAdmin)
admin.site.register(VideoCard, CategoryBaseAdmin)
admin.site.register(Memory, MemoryAdmin)
admin.site.register(Storage, StorageAdmin)
admin.site.register(OperatingSystem, CategoryBaseAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Ultrabooks, UltrabooksAdmin)
