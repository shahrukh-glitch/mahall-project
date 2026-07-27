import sqlite3
from flask import request, jsonify
from datetime import date

def init_expense_db():

    conn = sqlite3.connect("mahall.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expense(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
            expense_number TEXT NOT NULL ,
            expense_date TEXT NOT NULL,
            expense_category TEXT NOT NULL,
            expense_description TEXT NOT NULL,
            expense_amount REAL NOT NULL,
            payment_method TEXT NOT NULL,
            paid_to TEXT NOT NULL ,
            approved_by TEXT NOT NULL,
            remarks TEXT            
    ) 
    """)

    conn.commit()
    conn.close()

def save_expense():

    data = request.json

    allowed_categories = [
    "Electricity",
    "Water",
    "Internet",
    "Maintenance",
    "Cleaning",
    "Office Supplies",
    "Salary",
    "Charity",
    "Building",
    "Other"
    ]

    conn = sqlite3.connect("mahall.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT expense_number FROM expense
        ORDER BY id DESC
        LIMIT 1
        """)

    if data.get("expense_category") not in allowed_categories:
            conn.close()
            return jsonify({
                "message" : "Invalid Expense Categories"
                })

    existing_expense = cursor.fetchone()

    if not existing_expense:
        expense_number = "EX000001"
    else:
        latest_expense = existing_expense[0]
        number_part = latest_expense[2:]
        number = int(number_part)
        number += 1
        expense_number = f"EX{number:06d}"

    today = date.today()

    cursor.execute("""
    INSERT INTO expense(
        expense_number,
        expense_date,
        expense_category,
        expense_description,
        expense_amount,
        payment_method,
        paid_to,
        approved_by,
        remarks 
        )
        VALUES (?,?,?,?,?,?,?,?,?)  
        """,(
            expense_number,
            today,
            data.get("expense_category"),
            data.get("expense_description"),
            data.get("expense_amount"),
            data.get("payment_method"),
            data.get("paid_to"),
            data.get("approved_by"),
            data.get("remarks")
            ))

    conn.commit()
    conn.close()

    return jsonify({
         "message" : "Saved Successfully"
    })

#Temp
def view_expense():

    conn = sqlite3.connect("mahall.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM expense")

    rows = cursor.fetchall()

    conn.close()

    return jsonify(rows)

def search_expense(search_value):

    conn = sqlite3.connect('mahall.db')
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM expense
    WHERE expense_number = ?
    OR expense_date = ?
    """,(search_value,search_value)
    )

    donation = cursor.fetchall()

    conn.close()

    if donation:
        return jsonify (donation)
    else:
        return jsonify({
            "message" : "No Records Found"
        })

def update_expense():

    data = request.json

    conn = sqlite3.connect("mahall.db")
    cursor = conn.cursor()

    cursor.execute("""
            SELECT * FROM expense
            WHERE id = ?
            """,(
                data.get("id"),
            ))
    rows = cursor.fetchone()
    
    if rows:
        allowed_categories = [
            "Electricity",
            "Water",
            "Internet",
            "Maintenance",
            "Cleaning",
            "Office Supplies",
            "Salary",
            "Charity",
            "Building",
            "Other"
            ]

        if data.get("expense_category") not in allowed_categories:
            conn.close()
            return jsonify({
                "message" : "Invalid Expense Category"
            })
        cursor.execute("""
        UPDATE expense
        SET expense_category = ?,
            expense_description = ?,
            expense_amount = ?,
            payment_method = ?,
            paid_to = ?,
            approved_by = ?,
            remarks = ? 
        WHERE id = ?
        """,(
          data.get("expense_category"),
          data.get("expense_description"),
          data.get("expense_amount"),
          data.get("payment_method"),
          data.get("paid_to"),
          data.get("approved_by"),
          data.get("remarks"),
          data.get("id")
        ))

        conn.commit()
        conn.close()

        return jsonify({
            "message" : "Updated Successfully"
        })
    else:
        conn.close()
        return jsonify({
            "message" : "No Records Found"
        })

def delete_expense():
     
     data = request.json

     conn = sqlite3.connect("mahall.db")
     cursor = conn.cursor()

     cursor.execute("""
        SELECT id FROM expense
        WHERE id = ?
        """,(
             data.get("id"),
        ))
     existing_expense = cursor.fetchone()

     if existing_expense:
          cursor.execute("""
            DELETE FROM expense
            WHERE id = ?  
            """,(
                 data.get("id"),
            ))
          conn.commit()
          conn.close()

          return jsonify({
          "message" : "Deleted Successfully"
           })
     else:
          conn.close()
          return jsonify({
               "message" : "Expense Not Found"
          })







