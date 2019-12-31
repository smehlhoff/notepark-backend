import uuid
from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.signals import user_logged_in
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from .managers import CustomUserManager
from .utils import get_ip_address, get_user_agent


class User(AbstractUser):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    token_identifier = models.UUIDField(
        default=uuid.uuid4, editable=True, unique=True)
    is_banned = models.BooleanField(
        default=False,
        verbose_name='Banned',
        help_text='Designates whether the user account is accessible or not.'
    )

    objects = CustomUserManager()

    class Meta:
        db_table = 'users'
        verbose_name = 'user'
        verbose_name_plural = 'users'
        ordering = ['-date_joined']

    # https://github.com/GetBlimp/django-rest-framework-jwt/issues/385
    def generate_token_identifier(self):
        new_token_identifier = uuid.uuid4()
        self.token_identifier = new_token_identifier
        self.save()

        return self.token_identifier

    @property
    def token(self):
        return self.generate_jwt_token()

    def generate_jwt_token(self):
        # https://tools.ietf.org/html/rfc7519#section-4.1
        token = jwt.encode({
            'iss': settings.SITE_URL,
            'sub': self.username,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(minutes=1),
            'jti': str(self.token_identifier)
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')

    def __str__(self):
        return self.username


class UserProfile(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    ultrabook = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)
    bio = models.TextField(max_length=2500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users_profiles'
        verbose_name = 'user profile'
        verbose_name_plural = 'user profiles'
        ordering = ['-created_at']

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.update_or_create(user=instance)


class UserActivity(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField(
        max_length=255,
        unpack_ipv4=True,
        blank=True,
        null=True,
        verbose_name='IP address'
    )
    user_agent = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users_activity'
        verbose_name = 'user activity'
        verbose_name_plural = 'user activities'
        ordering = ['-created_at']

    def __str__(self):
        return self.user.username


def log_user_activity(sender, request, user, **kwargs):
    ip_address = get_ip_address(request)
    user_agent = get_user_agent(request)

    user_activity_details = UserActivity(
        user=user, ip_address=ip_address, user_agent=user_agent)
    user_activity_details.save()


user_logged_in.connect(log_user_activity)
