import uuid

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import F
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .managers import CommentManager


class Comment(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    content = models.TextField(max_length=2500)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=255)
    content_object = GenericForeignKey('content_type', 'object_id')
    public = models.BooleanField(default=True)
    report_count = models.PositiveIntegerField(default=0)
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

    objects = CommentManager()

    class Meta:
        db_table = 'comments'
        verbose_name = 'comment'
        verbose_name_plural = 'comments'
        ordering = ['-created_at']

    def __str__(self):
        return 'Comment by {user}'.format(user=self.user)


@receiver(post_save, sender=Comment)
def comment_count_create(sender, instance, created, **kwargs):
    if created:
        instance.content_object.__class__.objects.filter(id=instance.object_id).update(
            comment_count=F('comment_count') + 1
        )


@receiver(post_delete, sender=Comment)
def comment_count_delete(sender, instance, **kwargs):
    instance.content_object.__class__.objects.filter(id=instance.object_id).update(
        comment_count=F('comment_count') - 1
    )
