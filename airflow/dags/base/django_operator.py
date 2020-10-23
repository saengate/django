import os
import sys

from airflow.models import BaseOperator


def setup_django_for_airflow():
    # Add Django project root to path
    sys.path.append('/webapps/django/')

    environment = os.getenv('ENV', 'local')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.' + environment)

    import django
    django.setup()


class DjangoOperator(BaseOperator):

    def pre_execute(self, *args, **kwargs):
        setup_django_for_airflow()
