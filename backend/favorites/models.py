import uuid

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import F
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


class Favorite(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=255)
    content_object = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'favorites'
        verbose_name = 'favorite'
        verbose_name_plural = 'favorites'
        unique_together = ('user', 'content_type', 'object_id')
        ordering = ['-created_at']

    def __str__(self):
        return 'Favorite by {user}'.format(user=self.user)


@receiver(post_save, sender=Favorite)
def favorite_count_create(sender, instance, created, **kwargs):
    if created:
        instance.content_object.__class__.objects.filter(id=instance.object_id).update(
            favorite_count=F('favorite_count') + 1
        )


@receiver(post_delete, sender=Favorite)
def favorite_count_delete(sender, instance, **kwargs):
    instance.content_object.__class__.objects.filter(id=instance.object_id).update(
        favorite_count=F('favorite_count') - 1
    )
