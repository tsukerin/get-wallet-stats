import psycopg2
from psycopg2 import sql

conn_params = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': '5502',
    'host': 'localhost',
    'port': '5432'
}

conn = psycopg2.connect(**conn_params)
cur = conn.cursor()

def insert_wallet(wallet):
    check_query = sql.SQL("""
        SELECT 1 FROM wallets WHERE address = %s
    """)

    cur.execute(check_query, (wallet,))
    result = cur.fetchone()

    if result:
        print("Адрес уже существует в базе данных.")
    else:
        insert_query = sql.SQL("""
            INSERT INTO wallets (address)
            VALUES (%s)
        """)
        cur.execute(insert_query, (wallet,))
        conn.commit()
        print("Адрес успешно вставлен.")

# def get_wallet(wallet):
#     query