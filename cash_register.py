import sqlite3
from flask import request,jsonify

def init_cash_register_db():

    conn = sqlite3.connect("mahall.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cash_register(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    transaction_date TEXT NOT NULL,
    voucher_number TEXT NOT NULL,
    transaction_type TEXT NOT NULL,
    description TEXT NOT NULL,
    money_in REAL NOT NULL,
    money_out REAL NOT NULL,
    balance REAL NOT NULL
    )
    """)

    conn.commit()
    conn.close()

def add_cash_transaction(
    transaction_date,
    voucher_number,
    transaction_type,
    description,
    money_in,
    money_out
):
    conn = sqlite3.connect("mahall.db")
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT balance
    FROM cash_register 
    ORDER BY id DESC
    LIMIT 1""")
    
    latest_balance = cursor.fetchone()
    
    if latest_balance is None:
        latest_balance = 0

    else:
        latest_balance = latest_balance[0]

    money_in = float(money_in)
    money_out = float(money_out)
    
    new_balance = latest_balance + money_in - money_out

    cursor.execute("""
    INSERT INTO cash_register(
        transaction_date,
        voucher_number,
        transaction_type,
        description,
        money_in,
        money_out,
        balance)
        VALUES (?,?,?,?,?,?,?)
        """,(
            transaction_date,
            voucher_number,
            transaction_type,
            description,
            money_in,
            money_out,
            new_balance
            ))

    conn.commit()
    conn.close()

def view_cash_register():

    conn = sqlite3.connect("mahall.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM cash_register
    ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return jsonify(rows)
    