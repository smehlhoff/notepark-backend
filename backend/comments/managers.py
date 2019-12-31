from django.db import models


class CommentManager(models.Manager):
    def get_queryset(self):
        return super(CommentManager, self).get_queryset().filter(public=True)
