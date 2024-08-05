from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import time

def get_ton_balance(wallet):
    balance = None
    amount = None
    try:
        price_response = requests.get('https://tonapi.io/v2/rates?tokens=ton&currencies=usd')
        price_response.raise_for_status()
        balance_response = requests.get(f'https://tonapi.io/v2/accounts/{wallet}')
        balance_response.raise_for_status()
        
        price = price_response.json()['rates']['TON']['prices']['USD']
        balance = balance_response.json()['balance'] / 10**9 * price
        amount = round(balance_response.json()['balance'] / 10**9, 2)
    except requests.RequestException as e:
        print(f"Error: {e}")
        time.sleep(1)
        return get_ton_balance(wallet)
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    return balance, amount


def get_wallet_info(wallet):
    res = requests.get(f'https://tonapi.io/v2/accounts/{wallet}/jettons')
    return res.json()['balances']

def get_balance(balances, wallet):
    total = 0
    try:
        for i in balances:
            if int(i['balance']) > 0:
                    jetton = requests.get(f'https://tonapi.io/v2/accounts/{wallet}/jettons/{i["jetton"]["address"]}?currencies=usd').json()
                    total += (int(jetton['balance']) / 10**jetton['jetton']['decimals']) * jetton['price']['prices']['USD']
    except:
        time.sleep(1)
        get_balance(balances, wallet)
    total += get_ton_balance(wallet)[0]
    return round(total, 2)

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