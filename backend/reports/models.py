import uuid

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import F
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

CATEGORIES = (
    ('', ''),
    ('Advertising', 'Advertising'),
    ('Inappropriate', 'Inappropriate'),
    ('Spam', 'Spam'),
)


class Report(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=255)
    content_object = GenericForeignKey('content_type', 'object_id')
    category = models.CharField(max_length=255, choices=CATEGORIES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'reports'
        verbose_name = 'report'
        verbose_name_plural = 'reports'
        unique_together = ('user', 'content_type', 'object_id')
        ordering = ['-created_at']

    def __str__(self):
        return 'Report by {user}'.format(user=self.user)


@receiver(post_save, sender=Report)
def report_count_create(sender, instance, created, **kwargs):
    if created:
        instance.content_object.__class__.objects.filter(id=instance.object_id).update(
            report_count=F('report_count') + 1
        )


@receiver(post_delete, sender=Report)
def report_count_delete(sender, instance, **kwargs):
    instance.content_object.__class__.objects.filter(id=instance.object_id).update(
        report_count=F('report_count') - 1
    )
