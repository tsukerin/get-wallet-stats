from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from handlers.utils import *
import requests
import time

def get_wallet():
    with open('dags/cache', mode='r') as cache:
        return cache.readline()

def extract_balance(**kwargs):
    ti = kwargs['ti']

    wallet = get_wallet()
    info = get_wallet_info(wallet)
    balance = get_balance(info, wallet)

    ti.xcom_push(key='balance', value=balance)

def print_balance(**kwargs):
    ti = kwargs['ti']

    balance = ti.xcom_pull(key='balance', task_ids=['extract_balance'])
    print(balance)

with DAG('print_balance', description='test', catchup=False) as dag:
    extract_balance = PythonOperator(task_id='extract_balance', python_callable=extract_balance)
    print_balance = PythonOperator(task_id='print_balance', python_callable=print_balance)

    extract_balance >> print_balance