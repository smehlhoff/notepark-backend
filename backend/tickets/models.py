import uuid

from django.db import models

CATEGORIES = (
    ('', ''),
    ('Business', 'Business'),
    ('Feedback', 'Feedback'),
    ('Support', 'Support'),
    ('Tip-off', 'Tip-off'),
)

STATUS = (
    ('', ''),
    ('Closed', 'Closed'),
    ('Open', 'Open'),
)


class Ticket(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255, default='Created by admin')
    email = models.EmailField(max_length=255)
    category = models.CharField(max_length=255, choices=CATEGORIES)
    content = models.TextField(max_length=2500)
    status = models.CharField(max_length=255, choices=STATUS, default='Open')
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
        db_table = 'tickets'
        verbose_name = 'ticket'
        verbose_name_plural = 'tickets'
        ordering = ['-created_at']

    def __str__(self):
        return 'Ticket by {name}'.format(name=self.name.title())
