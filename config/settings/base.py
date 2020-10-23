import os

from config.core_settings import *  # NOQA

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# Refer to secret from project Secrets usually PROJECTNAME_SECRET

SECRET_KEY = os.getenv(
    'SECRET_KEY', "e7(sinr28hr10@9(+765wd&*0jjl%_qj1sxckjw!ssn^x0dm7@")

INSTALLED_APPS = INSTALLED_APPS + [  # NOQA
    'ses',
]
