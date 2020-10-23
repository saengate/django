import datetime as dt
import logging

from airflow import DAG
from base.django_operator import DjangoOperator


class DjangoExampleOperator(DjangoOperator):

    def execute(self, context):
        # from myApp.models import model
        # model.objects.get_or_create()
        from django.utils.translation import gettext as _

        from ses import msgs

        logger = logging.getLogger(__name__)
        logger.info(_(f"Tareas con funciones desde django en Airflow: {msgs.I.TEST_LOG}"))
        print("Iniciand tarea en operador Django!")
        print(msgs.I.TEST_LOG)
        print("Finalizando tarea en operador Django!")
        return True


default_args = {
    'start_date': dt.datetime(2020, 10, 7),
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=5),
}

with DAG(
    'test_dag_django',
    schedule_interval='0 * * * *',
    default_args=default_args,
) as dag:
    print_django = DjangoExampleOperator(
        task_id="hello_world",
    )

print_django
