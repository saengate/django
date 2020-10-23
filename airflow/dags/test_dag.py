""" import requests
import json

DAG_ID = 'test_dag'
headers = {
    'Cache-Control: no-cache',
    'Content-Type: application/json',
}
url = f'http://localhost:8080/api/experimental/dags/{DAG_ID}/dag_runs'
data = {}
response = requests.post(url, data=json.dumps(data), headers=headers) """

import datetime as dt
import pprint

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago


pp = pprint.PrettyPrinter(indent=4)


def hello_world():
    pp.print("Hello world!")
    return True


default_args = {
    'start_date': days_ago(2),
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=1),
}

with DAG(
    'test_dag',
    schedule_interval='@once',
    default_args=default_args,
) as dag:
    print_world = PythonOperator(
        task_id="hello_world",
        python_callable=hello_world,
    )

print_world
