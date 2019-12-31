from django.contrib import admin

from .models import Ticket


def set_tickets_open(modeladmin, request, queryset):
    rows_updated = queryset.update(status='Open')

    if rows_updated == 1:
        modeladmin.message_user(request, 'Ticket successfully set to open.')
    else:
        modeladmin.message_user(
            request, '{rows} tickets successfully set to open.'.format(rows=rows_updated))


set_tickets_open.short_description = 'Set open to selected tickets'


def set_tickets_closed(modeladmin, request, queryset):
    rows_updated = queryset.update(status='Closed')

    if rows_updated == 1:
        modeladmin.message_user(request, 'Ticket successfully set to closed.')
    else:
        modeladmin.message_user(
            request, '{rows} tickets successfully set to closed.'.format(rows=rows_updated))


set_tickets_closed.short_description = 'Set closed to selected tickets'


class TicketsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'category',
                    'status', 'created_at', 'updated_at')
    search_fields = ('content',)
    list_filter = ('category', 'status', 'created_at')
    fields = ('id', 'name', 'email', 'category', 'content', 'status', 'ip_address', 'user_agent', 'created_at',
              'updated_at')
    readonly_fields = ('id', 'ip_address', 'user_agent',
                       'created_at', 'updated_at')
    ordering = ('-created_at',)
    actions = [set_tickets_open, set_tickets_closed]

    def get_actions(self, request):
        actions = super(TicketsAdmin, self).get_actions(request)

        if not request.user.is_superuser and 'delete_selected' in actions:
            actions.pop('delete_selected')

        return actions


admin.site.register(Ticket, TicketsAdmin)
