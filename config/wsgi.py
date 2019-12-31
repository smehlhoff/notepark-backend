import os

from django.conf import settings
from django.core.wsgi import get_wsgi_application
from raven import Client
from raven.middleware import Sentry
from raven.transport.http import HTTPTransport

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')

application = get_wsgi_application()

if os.environ.get('DJANGO_SETTINGS_MODULE') == 'config.settings.production':
    application = Sentry(get_wsgi_application(), Client(
        dsn=settings.SENTRY_DSN, transport=HTTPTransport))
