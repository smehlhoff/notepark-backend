from .base import *

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '10.0.0.2']

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'dev',
        'USER': 'dev',
        'PASSWORD': 'dev',
        'HOST': '192.168.1.100',
        'PORT': '5432',
    },
}

DEBUG = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_PORT = 25

SECRET_KEY = 'jr7)nuw^&47$z@+h7^yd-np22p)8e_2e)i&3y#z8br_ae_yr(c'
