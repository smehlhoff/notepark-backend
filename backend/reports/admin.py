from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Report


class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'category', 'object_link', 'created_at')
    list_filter = ('category', 'created_at')
    fields = ('id', 'user', 'category', 'content_type',
              'object_id', 'created_at', 'updated_at')
    readonly_fields = ('id', 'user', 'object_link', 'created_at', 'updated_at')
    ordering = ('-created_at',)

    def get_queryset(self, request):
        queryset = self.model._base_manager.get_queryset()
        ordering = self.get_ordering(request)

        if ordering:
            return queryset.order_by(*ordering)

        return queryset

    def get_actions(self, request):
        actions = super(ReportAdmin, self).get_actions(request)

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


admin.site.register(Report, ReportAdmin)
