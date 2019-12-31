from django.db import models


class NewsManager(models.Manager):
    def get_queryset(self):
        return super(NewsManager, self).get_queryset().filter(public=True)
