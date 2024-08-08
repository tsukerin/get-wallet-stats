from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from handlers.utils import *
from datetime import datetime, timedelta
import random

def get_wallet_balance():

    hook = PostgresHook(postgres_conn_id='wallet_db')
    conn = hook.get_conn()
    cursor = conn.cursor()
    
    select_query = "SELECT id FROM wallets"
    cursor.execute(select_query)
    wallets = cursor.fetchall()

    insert_query = """
        INSERT INTO five_m (wallet_id, value, date)
        VALUES (%s, %s, %s)
    """
    for wallet in wallets:
        wallet_id = wallet[0]
        
        info = get_wallet_info(wallet)
        balance = get_balance(info, wallet)

        created_at = datetime.now()
        cursor.execute(insert_query, (wallet_id, balance, created_at))
    
    conn.commit()
    cursor.close()
    conn.close()

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 8, 8),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'five_mins_monitor',
    default_args=default_args,
    schedule_interval=timedelta(minutes=5),
    catchup=False
)

five_mins_monitor = PythonOperator(
    task_id='five_mins_monitor',
    python_callable=get_wallet_balance,
    dag=dag,
)

five_mins_monitor
