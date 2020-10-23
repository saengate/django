import pygments

from config.settings.base import *  # NOQA
from os import getenv
from utils.color_logging import formatter
from neomodel import config


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ENVIRONMENT = 'develop'

print(ENVIRONMENT)
print(getenv('DJANGO_SETTINGS_MODULE'))

HOSTS = {
    'production': ['127.0.0.1'],
    'develop': ['127.0.0.1', '0.0.0.0', 'localhost'],
}

WS_ALLOWED_HOSTS = ['*'] if DEBUG else HOSTS[ENVIRONMENT]

ALLOWED_HOSTS = ['*']

# https://pypi.org/project/django_neomodel/
NEOMODEL_NEO4J_BOLT_URL = 'bolt://neo4j:neo4j@djfullapp-neo4j:7687'
NEOMODEL_SIGNALS = True
NEOMODEL_FORCE_TIMEZONE = False
NEOMODEL_ENCRYPTED_CONNECTION = True
config.MAX_POOL_SIZE = 50

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

"""
'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
}
"""

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

# ==============================================================================
# WEBSOCKETS & CHANNELS
# ==============================================================================

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
            'maxBytes': 1024 * 1024 * 10,  # 10MB
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
