import requests

def get_wallet_info(wallet):
    res = requests.get(f'https://tonapi.io/v2/accounts/{wallet}/jettons')
    return res.json()['balances']

def get_ton_balance(wallet):
    price = requests.get('https://tonapi.io/v2/rates?tokens=ton&currencies=usd')
    balance = requests.get(f'https://tonapi.io/v2/accounts/{wallet}').json()['balance'] / 10**9 * price.json()['rates']['TON']['prices']['USD']
    amount = round(requests.get(f'https://tonapi.io/v2/accounts/{wallet}').json()['balance'] / 10**9, 2)
    return balance, amount

def get_balance(balances, wallet):
    total = 0
    for i in balances:
        if int(i['balance']) > 0:
            try:
                jetton = requests.get(f'https://tonapi.io/v2/accounts/{wallet}/jettons/{i["jetton"]["address"]}?currencies=usd').json()
                total += (int(jetton['balance']) / 10**jetton['jetton']['decimals']) * jetton['price']['prices']['USD']
            except KeyError('balance'):
                continue
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