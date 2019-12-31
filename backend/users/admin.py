from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import gettext_lazy as _

from .models import User, UserProfile, UserActivity


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class CustomUserCreationForm(UserCreationForm):
    error_message = UserCreationForm.error_messages.update({
        'duplicate_username': 'This username already exists.'
    })

    class Meta(UserCreationForm.Meta):
        model = User

    def clean_username(self):
        username = self.cleaned_data['username']

        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username

        raise forms.ValidationError(self.error_messages['duplicate_username'])


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name',
                    'last_name', 'is_staff', 'is_banned')
    list_filter = ('is_banned', 'is_staff', 'is_superuser', 'groups')
    fieldsets = (
        (None, {'fields': ('username', 'password', 'token_identifier')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_banned', 'is_active', 'is_staff', 'is_superuser', 'groups',
                                       'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )
    readonly_fields = ('token_identifier',)
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at')
    search_fields = ('user',)
    list_filter = ('user', 'created_at')
    fields = ('id', 'user', 'ultrabook', 'location',
              'bio', 'created_at', 'updated_at')
    readonly_fields = ('id', 'created_at', 'updated_at')
    ordering = ('-created_at',)


class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'ip_address', 'user_agent', 'created_at')
    search_fields = ('user',)
    list_filter = ('created_at',)
    fields = ('id', 'user', 'ip_address', 'user_agent', 'created_at')
    readonly_fields = ('id', 'user', 'ip_address', 'user_agent', 'created_at')
    ordering = ('-created_at',)


admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserActivity, UserActivityAdmin)
