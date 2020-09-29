"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 2.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import pygments.formatters
import os

from os import getenv
from rest_framework import compat


from utils.color_logging import formatter

# I have the same issue, but poetry does not allow me to update Markdown to from 2.6.11 to 3+
# because apache-airflow (1.10.10) depends on markdown (>=2.5.2,<3.0)
compat.md_filter_add_syntax_highlight = lambda md: False

ENVIRONMENT = 'develop'

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.abspath(BASE_DIR)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'e7(sinr28hr10@9(+765wd&*0jjl%_qj1sxckjw!ssn^x0dm7@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'channels',
    'django_neomodel',
    'easyaudit',
    'django_extensions',

    'ses',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'easyaudit.middleware.easyaudit.EasyAuditMiddleware',
]

ROOT_URLCONF = 'config.urls'


REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
        # 'rest_framework.permissions.DjangoModelPermissions',
        # 'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly,
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
}


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

"""
'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
}
"""
# https://pypi.org/project/django_neomodel/

NEOMODEL_NEO4J_BOLT_URL = 'bolt://neo4j:neo4j@djfullapp-neo4j:7687'
NEOMODEL_SIGNALS = True
NEOMODEL_FORCE_TIMEZONE = False
NEOMODEL_ENCRYPTED_CONNECTION = True
NEOMODEL_MAX_POOL_SIZE = 50

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'djfullappdb',
        'USER': 'userdb',
        'PASSWORD': 'password',
        'HOST': 'djfullapp-db',
        'PORT': '5432',
    },
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, 'staticfiles'),
]

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

# django-admin makemessages -a && django-admin compilemessages

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

LANGUAGE_CODE = 'es-cl'
# LANGUAGE_CODE = 'en-us'


def _(s): return s  # NOQA


LANGUAGES = [
    ('es', _('Espanish')),
    ('en', _('English')),
]


# ==============================================================================
# WEBSOCKETS & CHANNELS
# ==============================================================================

ASGI_APPLICATION = 'config.routing.application'

REDIS_HOST = getenv('REDIS_HOST', 'redis://redis:6379')

# It is possible to have multiple channel layers configured.
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [REDIS_HOST],
        },
    },
}

HOSTS = {
    'production': ['127.0.0.1'],
    'develop': ['127.0.0.1'],
}

WS_ALLOWED_HOSTS = ['*'] if DEBUG else HOSTS[ENVIRONMENT]


# LOGS
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': formatter(),
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/django/django.log',
            'maxBytes': 1024*1024*10,  # 10MB
            'backupCount': 5,
            'formatter': 'standard',
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
    },
    'loggers': {
        '': {
            'class': 'utils.color_logging.NewLogger',
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'console': {
            'class': 'utils.color_logging.NewLogger',
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'all': {
            'class': 'utils.color_logging.NewLogger',
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}


# AUDIT [django-easy-audit](https://github.com/soynatan/django-easy-audit)

DJANGO_EASY_AUDIT_WATCH_MODEL_EVENTS = True
DJANGO_EASY_AUDIT_WATCH_AUTH_EVENTS = True
DJANGO_EASY_AUDIT_WATCH_REQUEST_EVENTS = True

# DJANGO_EASY_AUDIT_UNREGISTERED_CLASSES_EXTRA = ['app_name.model_name']
# DJANGO_EASY_AUDIT_UNREGISTERED_URLS_EXTRA = ['url']
# DJANGO_EASY_AUDIT_CRUD_DIFFERENCE_CALLBACKS = ['string-paths-to-functions-classes']

# This is reserved for future use (does not do anything yet) 1.2.2
# DJANGO_EASY_AUDIT_USER_DB_CONSTRAINT = 'default'

# DJANGO_EASY_AUDIT_CRUD_EVENT_LIST_FILTER = ['event_type', 'content_type', 'user', 'datetime', ]
# DJANGO_EASY_AUDIT_LOGIN_EVENT_LIST_FILTER = ['login_type', 'user', 'datetime', ]
# DJANGO_EASY_AUDIT_REQUEST_EVENT_LIST_FILTER = ['method', 'user', 'datetime', ]

# DJANGO_EASY_AUDIT_DATABASE_ALIAS = 'default '

# No guarda auditoria si no han ocurrido cambios
DJANGO_EASY_AUDIT_CRUD_EVENT_NO_CHANGED_FIELDS_SKIP = True

# Solo lectura impide que un superusuario los modifique
DJANGO_EASY_AUDIT_READONLY_EVENTS = True

# DJANGO_EASY_AUDIT_LOGGING_BACKEND = 'easyaudit.backends.ModelBackend'

# https://django-extensions.readthedocs.io/en/latest/shell_plus.html
# ./manage.py shell_plus --notebook
# Always use IPython for shell_plus
SHELL_PLUS = "ipython"
SHELL_PLUS_PRINT_SQL = True
# Truncate sql queries to this number of characters (this is the default)
SHELL_PLUS_PRINT_SQL_TRUNCATE = 1000
# To disable truncation of sql queries use
SHELL_PLUS_PRINT_SQL_TRUNCATE = None
# Specify sqlparse configuration options when printing sql queries to the console
SHELL_PLUS_SQLPARSE_FORMAT_KWARGS = dict(
    reindent_aligned=True,
    truncate_strings=500,
)

# Specify Pygments formatter and configuration options when printing sql queries to the console
SHELL_PLUS_PYGMENTS_FORMATTER = pygments.formatters.TerminalFormatter
SHELL_PLUS_PYGMENTS_FORMATTER_KWARGS = {}

# Additional IPython arguments to use
IPYTHON_ARGUMENTS = [
    '--ext', 'django_extensions.management.notebook_extension',
    '--debug',
]

IPYTHON_KERNEL_DISPLAY_NAME = "Django Shell-Plus"
# Additional Notebook arguments to use
NOTEBOOK_ARGUMENTS = []
NOTEBOOK_KERNEL_SPEC_NAMES = ["python3", "python"]

NOTEBOOK_ARGUMENTS = [
    '--allow-root',
    '--ip', '0.0.0.0',
    '--port', '7001',
]
