from django.db import models


class UltrabooksManager(models.Manager):
    def get_queryset(self):
        return super(UltrabooksManager, self).get_queryset().filter(public=True)
