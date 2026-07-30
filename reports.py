import sqlite3
from flask import request,jsonify

def donation_reports():

    data = request.json

    month = data.get("month")
    year = data.get("year")

    conn = sqlite3.connect("mahall.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM donation
    WHERE strftime('%m', donation_date) = ?
    AND strftime('%Y', donation_date) = ?
    """, (
    month,
    year
    ))

    donation_records = cursor.fetchall()

    cursor.execute("""
    SELECT SUM(donation_amount)
    FROM donation
    WHERE strftime('%m', donation_date) = ?
    AND strftime('%Y', donation_date) = ?
    """, (
    month,
    year
    ))

    total_donation = cursor.fetchone()[0]

    if total_donation is None:
        total_donation = 0

    conn.close()
    return jsonify ({
        "donation_records": donation_records,
        "total_donation": total_donation
    })

def expense_reports():

    data = request.json

    month = data.get("month")
    year = data.get("year")

    conn = sqlite3.connect("mahall.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM expense
    WHERE strftime('%m', expense_date) = ?
    AND strftime('%Y', expense_date) = ?
    """, (
    month,
    year
    ))

    expense_records = cursor.fetchall()

    cursor.execute("""
    SELECT SUM(expense_amount)
    FROM expense
    WHERE strftime('%m', expense_date) = ?
    AND strftime('%Y', expense_date) = ?
    """, (
    month,
    year
    ))

    total_expense = cursor.fetchone()[0]

    if total_expense is None:
        total_expense = 0

    conn.close()
    return jsonify ({
        "expense_records": expense_records,
        "total_expense": total_expense
    })

def financial_summary():

    data = request.json

    month = data.get("month")
    year = data.get("year")

    conn = sqlite3.connect("mahall.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT SUM(donation_amount)
    FROM donation
    WHERE strftime('%m', donation_date) = ?
    AND strftime('%Y', donation_date) = ?
    """,(
        month,
        year
    ))

    total_donations = cursor.fetchone()[0]

    if total_donations is None:
        total_donations = 0

    cursor.execute("""
        SELECT SUM(expense_amount)
        FROM expense
        WHERE strftime('%m', expense_date) = ?
        AND strftime('%Y', expense_date) = ?
        """,(
            month,
            year
        ))
    
    total_expenses = cursor.fetchone()[0]
    
    if total_expenses is None:
            total_expenses = 0

    net_cash = total_donations - total_expenses

    cursor.execute("""
    SELECT COUNT (*)
    FROM donation
    WHERE strftime('%m', donation_date) = ?
    AND strftime('%Y', donation_date) = ?
    """,(
         month,
         year
    ))

    total_donation_transactions = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT (*)
        FROM expense
        WHERE strftime('%m', expense_date) = ?
        AND strftime('%Y', expense_date) = ?
        """,(
             month,
             year
        ))
    
    total_expense_transactions = cursor.fetchone()[0]

    conn.close()

    return jsonify({
    "total_donations": total_donations,
    "total_expenses": total_expenses,
    "net_cash": net_cash,
    "total_donation_transactions": total_donation_transactions,
    "total_expense_transactions": total_expense_transactions
    })
         

    
