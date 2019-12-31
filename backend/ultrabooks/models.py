import uuid

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from slugify import slugify

from backend.comments.models import Comment
from backend.favorites.models import Favorite
from .managers import UltrabooksManager


class Base(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CategoryBase(Base):
    name = models.CharField(unique=True, max_length=255)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Company(Base):
    name = models.CharField(unique=True, max_length=255)
    slug = models.SlugField(unique=True, max_length=255)

    class Meta:
        db_table = 'ultrabooks_company'
        verbose_name = 'company'
        verbose_name_plural = 'companies'
        ordering = ['name']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name.lower())
        super(Company, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Color(Base):
    color = models.CharField(unique=True, max_length=255)

    class Meta:
        db_table = 'ultrabooks_color'
        verbose_name = 'color'
        verbose_name_plural = 'colors'
        ordering = ['color']

    def __str__(self):
        return self.color


class Processor(CategoryBase):
    class Meta:
        db_table = 'ultrabooks_processor'
        verbose_name = 'processor'
        verbose_name_plural = 'processors'
        ordering = ['name']


class VideoCard(CategoryBase):
    class Meta:
        db_table = 'ultrabooks_video_card'
        verbose_name = 'video card'
        verbose_name_plural = 'video cards'
        ordering = ['name']


class Memory(Base):
    speed = models.CharField(unique=True, max_length=255)

    class Meta:
        db_table = 'ultrabooks_memory'
        verbose_name = 'memory'
        verbose_name_plural = 'memory'
        ordering = ['speed']

    def __str__(self):
        return self.speed


class Storage(Base):
    capacity = models.CharField(unique=True, max_length=255)

    class Meta:
        db_table = 'ultrabooks_storage'
        verbose_name = 'storage'
        verbose_name_plural = 'storage'
        ordering = ['capacity']

    def __str__(self):
        return self.capacity


class OperatingSystem(CategoryBase):
    class Meta:
        db_table = 'ultrabooks_operating_system'
        verbose_name = 'operating system'
        verbose_name_plural = 'operating systems'
        ordering = ['name']


class Image(Base):
    name = models.CharField(unique=True, max_length=255)
    slug = models.ImageField(
        unique=True, max_length=255, upload_to='ultrabooks/')

    class Meta:
        db_table = 'ultrabooks_image'
        verbose_name = 'image'
        verbose_name_plural = 'images'
        ordering = ['name']

    def __str__(self):
        return self.name


STATUS = (
    ('Draft', 'Draft'),
    ('Pending Review', 'Pending Review'),
    ('Published', 'Published'),
)


class Ultrabooks(Base):
    name = models.CharField(unique=True, max_length=255)
    slug = models.SlugField(unique=True, max_length=255)
    company = models.ForeignKey(
        Company, related_name='ultrabooks', on_delete=models.CASCADE)
    launch_date = models.DateField(auto_now=False, blank=True, null=True)
    weight = models.FloatField()
    dimensions = models.CharField(max_length=255)
    design_colors = models.ManyToManyField(Color)
    processor_models = models.ManyToManyField(Processor)
    video_card_models = models.ManyToManyField(VideoCard)
    memory_models = models.ManyToManyField(Memory)
    storage_models = models.ManyToManyField(Storage)
    display_size = models.CharField(max_length=255)
    display_resolution = models.CharField(max_length=255)
    battery = models.CharField(max_length=255)
    wireless = models.TextField()
    video = models.TextField()
    audio = models.TextField()
    connectivity = models.TextField()
    operating_system_models = models.ManyToManyField(OperatingSystem)
    optical_drive = models.CharField(max_length=255)
    features = models.TextField()
    images = models.ManyToManyField(Image)
    status = models.CharField(max_length=255, choices=STATUS)
    public = models.BooleanField(default=True)
    allow_comments = models.BooleanField(default=True)
    display_comments = models.BooleanField(default=True)
    comment_count = models.PositiveIntegerField(
        default=0, help_text='This includes comments set to private.')
    comments = GenericRelation(Comment)
    allow_favorites = models.BooleanField(default=True)
    display_favorites = models.BooleanField(default=True)
    favorite_count = models.PositiveIntegerField(default=0)
    favorites = GenericRelation(Favorite)

    objects = UltrabooksManager()

    class Meta:
        db_table = 'ultrabooks'
        verbose_name = 'ultrabook'
        verbose_name_plural = 'ultrabooks'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name.lower())
        super(Ultrabooks, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
