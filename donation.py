import sqlite3
from flask import request, jsonify
from datetime import date

def init_donation_db():

    conn = sqlite3.connect('mahall.db')
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS donation(
        
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        donation_number TEXT NOT NULL ,
        donor_name TEXT NOT NULL,
        donor_phone TEXT NOT NULL,
        donation_date TEXT NOT NULL,
        donation_type TEXT NOT NULL,
        donation_amount REAL NOT NULL,
        payment_method TEXT NOT NULL ,
        remarks TEXT,
        received_by TEXT NOT NULL            
        ) 
        """)

    conn.commit()
    conn.close()

def save_donation():

    data = request.json

    allowed_types = [
    "General Donation",
    "Friday Collection",
    "Zakat",
    "Sadaqah",
    "Building Fund",
    "Ramadan Fund",
    "Charity Fund"
    ]

    conn = sqlite3.connect('mahall.db')
    cursor = conn.cursor()

    cursor.execute("""
    SELECT donation_number FROM donation
    ORDER BY id DESC
    LIMIT 1
    """)

    if data.get("donation_type") not in allowed_types:
        conn.close()
        return jsonify({
            "message" : "Invalid Donation Type"
            })
    
    existing_donation = cursor.fetchone()

    if not existing_donation:
        donation_number = 'DN000001'
    else:
        latest_donation = existing_donation[0]
        number_part = latest_donation[2:]
        number = int(number_part)
        number += 1
        donation_number = f"DN{number:06d}"

    today = date.today()

    cursor.execute("""
    INSERT INTO donation(
        donation_number,
        donor_name,
        donor_phone,
        donation_date,
        donation_type,
        donation_amount,
        payment_method,
        remarks,
        received_by
        )
        VALUES(?,?,?,?,?,?,?,?,?)
        """,(
            donation_number,
            data.get('donor_name'),
            data.get('donor_phone'),
            today,
            data.get('donation_type'),
            data.get('donation_amount'),
            data.get('payment_method'),
            data.get('remarks'),
            data.get('received_by')
        ))

    conn.commit()
    conn.close()

    return jsonify({
        "message" : "Saved Successfully"
    })

#Temp
def view_donations():

    conn = sqlite3.connect("mahall.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM donation")

    rows = cursor.fetchall()

    conn.close()

    return jsonify(rows)

def search_donation(search_value):

    conn = sqlite3.connect('mahall.db')
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM donation
    WHERE donation_number = ?
    OR donor_name = ?
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

def update_donation():

    data = request.json

    conn = sqlite3.connect("mahall.db")
    cursor = conn.cursor()

    cursor.execute("""
            SELECT * FROM donation
            WHERE id = ?
            """,(
                data.get("id"),
            ))
    rows = cursor.fetchone()
    
    if rows:
        allowed_types = [
        "General Donation",
        "Friday Collection",
        "Zakat",
        "Sadaqah",
        "Building Fund",
        "Ramadan Fund",
        "Charity Fund"]

        if data.get("donation_type") not in allowed_types:
            conn.close()
            return jsonify({
                "message" : "Invalid Donation Type"
            })
        cursor.execute("""
        UPDATE donation
        SET donor_name = ?,
            donor_phone = ?,
            donation_type = ?,
            donation_amount = ?,
            payment_method = ?,
            remarks = ?,
            received_by = ?
        WHERE id = ?
        """,(
          data.get("donor_name"),
          data.get("donor_phone"),
          data.get("donation_type"),
          data.get("donation_amount"),
          data.get("payment_method"),
          data.get("remarks"),
          data.get("received_by"),
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

def delete_donation():
     
     data = request.json

     conn = sqlite3.connect("mahall.db")
     cursor = conn.cursor()

     cursor.execute("""
        SELECT id FROM donation
        WHERE id = ?
        """,(
             data.get("id"),
        ))
     existing_donation = cursor.fetchone()

     if existing_donation:
          cursor.execute("""
            DELETE FROM donation
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
               "message" : "Donation Not Found"
          })

