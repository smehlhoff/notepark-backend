import uuid
from datetime import datetime

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from slugify import slugify

from backend.comments.models import Comment
from .managers import NewsManager
from .utils import get_read_time

STATUS = (
    ('Draft', 'Draft'),
    ('Pending Review', 'Pending Review'),
    ('Published', 'Published'),
)


class News(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(unique_for_date='created_at', max_length=255)
    slug = models.SlugField(unique_for_date='created_at', max_length=255)
    content = models.TextField()
    read_time = models.TimeField(blank=True, null=True)
    status = models.CharField(max_length=255, choices=STATUS)
    public = models.BooleanField(default=True)
    allow_comments = models.BooleanField(default=True)
    display_comments = models.BooleanField(default=True)
    comment_count = models.PositiveIntegerField(
        default=0, help_text='This includes comments set to private.')
    comments = GenericRelation(Comment)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = NewsManager()

    class Meta:
        db_table = 'news'
        verbose_name = 'news'
        verbose_name_plural = 'news'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        now = datetime.utcnow()

        self.slug = '{year}/{month}/{day}/{slug}'.format(
            year=now.year,
            month=now.month,
            day=now.day,
            slug=slugify(self.title.lower())
        )

        self.read_time = get_read_time(self.content)
        super(News, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
