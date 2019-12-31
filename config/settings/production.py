from .base import *

SECRET_KEY = os.environ.get('SECRET_KEY')

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS')

CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True
CSRF_USE_SESSIONS = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('RDS_DB_NAME'),
        'USER': os.environ.get('RDS_USERNAME'),
        'PASSWORD': os.environ.get('RDS_PASSWORD'),
        'HOST': os.environ.get('RDS_HOSTNAME'),
        'PORT': os.environ.get('RDS_PORT'),
    },
}

DATABASES['default']['ATOMIC_REQUESTS'] = True
DATABASES['default']['CONN_MAX_AGE'] = 300

DEBUG = False

EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_USE_TLS = True

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
# https://wiki.mozilla.org/Security/Guidelines/Web_Security#HTTP_Strict_Transport_Security
SECURE_HSTS_SECONDS = 63072000
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True

X_FRAME_OPTIONS = 'DENY'

# Default Logging

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'verbose': {
#             'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
#         },
#         'simple': {
#             'format': '%(levelname)s %(message)s'
#         },
#     },
#     'filters': {
#         'special': {
#             '()': 'project.logging.SpecialFilter',
#             'foo': 'bar',
#         },
#         'require_debug_true': {
#             '()': 'django.utils.log.RequireDebugTrue',
#         },
#     },
#     'handlers': {
#         'console': {
#             'level': 'INFO',
#             'filters': ['require_debug_true'],
#             'class': 'logging.StreamHandler',
#             'formatter': 'simple'
#         },
#         'mail_admins': {
#             'level': 'ERROR',
#             'class': 'django.utils.log.AdminEmailHandler',
#             'filters': ['special']
#         }
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['console'],
#             'propagate': True,
#         },
#         'django.request': {
#             'handlers': ['mail_admins'],
#             'level': 'ERROR',
#             'propagate': False,
#         },
#         'notepark.custom': {
#             'handlers': ['console', 'mail_admins'],
#             'level': 'INFO',
#             'filters': ['special']
#         }
#     }
# }

# Sentry

INSTALLED_APPS += ['raven.contrib.django.raven_compat', ]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'ERROR',  # INFO, WARNING, ERROR, etc.
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            'tags': {'custom-tag': 'x'},
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}

RAVEN_CONFIG = {
    'dsn': os.environ.get('SENTRY_DSN')
}

# django-storages

INSTALLED_APPS += ['storages', ]

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID_BUCKET')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY_BUCKET')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_AUTO_CREATE_BUCKET = True
AWS_QUERYSTRING_AUTH = False

# https://developers.google.com/web/fundamentals/performance/optimizing-content-efficiency/http-caching#cache-control
# 86400 = (60 seconds x 60 minutes x 24 hours)
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

MEDIAFILES_LOCATION = 'media'
MEDIA_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)
DEFAULT_FILE_STORAGE = 'config.storage.MediaStorage'

STATICFILES_LOCATION = 'static'
STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, STATICFILES_LOCATION)
STATICFILES_STORAGE = 'config.storage.StaticStorage'
