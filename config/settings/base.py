import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# CORE SETTINGS

ADMIN_SITE_HEADER = 'notepark'
ADMIN_SITE_INDEX_TITLE = 'Site administration'
ADMIN_SITE_TITLE = 'notepark'

ADMINS = [('admin', 'admin@notepark.net')]
MANAGERS = ADMINS

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_FROM = 'admin@notepark.net'
EMAIL_SUBJECT_PREFIX = ''

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.postgres',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'backend.comments',
    'backend.favorites',
    'backend.news',
    'backend.reports',
    'backend.tickets',
    'backend.ultrabooks',
    'backend.users',
]

LANGUAGE_CODE = 'en-us'

MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'media')

MEDIA_URL = '/media/'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'backend.users.backends.JWTAuthentication',
    ),
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100,
    'NON_FIELD_ERRORS_KEY': 'error',
    'EXCEPTION_HANDLER': 'config.exceptions.custom_exception_handler',
}

ROOT_URLCONF = 'config.urls'

SITE_NAME = 'notepark.net'
SITE_URL = 'https://notepark.net'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(os.path.dirname(BASE_DIR), 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.media',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

TIME_ZONE = 'UTC'

USE_I18N = False

USE_L10N = True

USE_TZ = True

WSGI_APPLICATION = 'config.wsgi.application'

# AUTH SETTINGS

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

AUTH_USER_MODEL = 'users.User'

PASSWORD_RESET_TIMEOUT_DAYS = 1

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
]

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

TOKEN_PREFIX = 'Bearer'

# STATIC FILES

STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'staticfiles')

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(os.path.dirname(BASE_DIR), 'static'),
]

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]
