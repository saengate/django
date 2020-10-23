import datetime as dt

from airflow import DAG
from airflow.operators.python_operator import PythonOperator


def hello_world():
    print("Hello world scheduler testing!")
    return True


default_args = {
    'start_date': dt.datetime(2020, 10, 7),
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=1),
}

with DAG(
    'test_dag_scheduler',
    schedule_interval='*/1 * * * *',
    default_args=default_args,
) as dag:
    print_world = PythonOperator(
        task_id="hello_world",
        python_callable=hello_world,
    )

print_world
