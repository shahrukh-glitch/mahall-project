import sqlite3
from flask import request,jsonify
from datetime import date

def dashboard():

    conn = sqlite3.connect("mahall.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT (*)
    FROM member_registration
    """)

    total_families = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT (*)
    FROM family_members
    """)

    total_family_members = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT (*)
    FROM usthad
    """)

    total_usthads = cursor.fetchone()[0]

    today = date.today()

    cursor.execute("""
    SELECT SUM(donation_amount)
    FROM donation
    WHERE donation_date = ?
    """, (today,))

    todays_donations = cursor.fetchone()[0]

    if todays_donations is None:
        todays_donations = 0

    cursor.execute("""
    SELECT SUM(expense_amount)
        FROM expense
        WHERE expense_date = ?
        """, (today,))

    todays_expenses = cursor.fetchone()[0]
    
    if todays_expenses is None:
        todays_expenses = 0

    current_month = f"{today.month:02d}"
    current_year = str(today.year)

    cursor.execute("""
        SELECT SUM(donation_amount)
            FROM donation
            WHERE strftime('%m', donation_date) = ?
            AND strftime('%Y', donation_date) = ?
            """, (current_month,current_year))

    month_donations = cursor.fetchone()[0]

    if month_donations is None:
        month_donations = 0

    cursor.execute("""
            SELECT SUM(expense_amount)
                FROM expense
                WHERE strftime('%m', expense_date) = ?
                AND strftime('%Y', expense_date) = ?
                """, (current_month,current_year))
    
    month_expenses = cursor.fetchone()[0]
    
    if month_expenses is None:
        month_expenses = 0

    net_cash = month_donations - month_expenses

    conn.close()

    return jsonify ({
        "total_families": total_families,
        "total_family_members": total_family_members,
        "total_usthads": total_usthads,
        "todays_donations": todays_donations,
        "todays_expenses": todays_expenses,
        "month_donation": month_donations,
        "month_expenses": month_expenses,
        "net_cash": net_cash
    })