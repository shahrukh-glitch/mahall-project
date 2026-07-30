import sqlite3
from flask import request,jsonify

def ledger():

    data = request.json

    ledger_type = data.get("ledger_type")
    month = data.get("month")
    year = data.get("year")

    conn = sqlite3.connect("mahall.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT transaction_date,
    voucher_number,
    transaction_type,
    description,
    money_in,
    money_out
    FROM cash_register
    WHERE transaction_type = ?
    AND strftime('%m', transaction_date) = ?
    AND strftime('%Y', transaction_date) = ?
    """,(
        ledger_type,
        month,
        year
    ))

    ledger_records = cursor.fetchall()

    cursor.execute("""
    SELECT SUM(money_in)
    FROM cash_register
    WHERE  transaction_type = ?
    AND strftime('%m', transaction_date) = ?
    AND strftime('%Y', transaction_date) = ?
    """,(
        ledger_type,
        month,
        year
    ))

    total_money_in = cursor.fetchone()[0]

    if total_money_in is None:
        total_money_in = 0

    cursor.execute("""
        SELECT SUM(money_out)
        FROM cash_register
        WHERE  transaction_type = ?
        AND strftime('%m', transaction_date) = ?
        AND strftime('%Y', transaction_date) = ?
        """,(
            ledger_type,
            month,
            year
        ))
    
    total_money_out = cursor.fetchone()[0]
    
    if total_money_out is None:
            total_money_out = 0

    conn.close()

    return jsonify({
       "ledger_records": ledger_records,
       "total_money_in": total_money_in,
       "total_money_out": total_money_out
    })

def cash_flow():

    data = request.json

    month = data.get("month")
    year = data.get("year")

    conn = sqlite3.connect("mahall.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT SUM(money_in)
        FROM cash_register
        WHERE strftime('%m', transaction_date) = ?
        AND strftime('%Y', transaction_date) = ?
        """,(
            month,
            year
        ))
    
    total_money_in = cursor.fetchone()[0]
    
    if total_money_in is None:
            total_money_in = 0

    cursor.execute("""
            SELECT SUM(money_out)
            FROM cash_register
            WHERE strftime('%m', transaction_date) = ?
            AND strftime('%Y', transaction_date) = ?
            """,(
                month,
                year
            ))
        
    total_money_out = cursor.fetchone()[0]
        
    if total_money_out is None:
                total_money_out = 0

    net_cash_flow = total_money_in - total_money_out

    conn.close()

    return jsonify({
           "total_money_in": total_money_in,
            "total_money_out": total_money_out,
            "net_cash_flow": net_cash_flow
    })