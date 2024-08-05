import requests
import time

def get_wallet_info(wallet):
    res = requests.get(f'https://tonapi.io/v2/accounts/{wallet}/jettons')
    return res.json()['balances']

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

def get_jettons(balances, wallet):
    jettons = []
    for i in balances:
        if int(i['balance']) > 0:
            jetton = requests.get(f'https://tonapi.io/v2/accounts/{wallet}/jettons/{i["jetton"]["address"]}?currencies=usd').json()
            jettons.append([
                jetton['jetton']['image'], jetton['jetton']['name'], round(int(jetton['balance']) / 10**jetton['jetton']['decimals'], 2),
                round((int(jetton['balance']) / 10**jetton['jetton']['decimals']) * jetton['price']['prices']['USD'], 2)
            ])
    return jettons