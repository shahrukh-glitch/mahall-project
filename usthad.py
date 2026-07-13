import sqlite3
from flask import request, jsonify

def init_usthad_db():

    conn = sqlite3.connect("mahall.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usthad(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        photo TEXT NOT NULL,
        phone TEXT NOT NULL,
        address TEXT NOT NULL,
        aadhaar_number TEXT NOT NULL UNIQUE,
        date_of_birth TEXT NOT NULL,
        gender TEXT NOT NULL,
        education TEXT NOT NULL,
        islamic_education TEXT NOT NULL,
                   
            employee_id TEXT NOT NULL UNIQUE,
            position TEXT NOT NULL,
            mahall_role TEXT NOT NULL,
            date_of_joining TEXT NOT NULL,
            employment_status TEXT NOT NULL,
            
                basic_salary REAL NOT NULL,
                allowance REAL NOT NULL DEFAULT 0,
                deduction REAL NOT NULL DEFAULT 0,
                net_salary REAL NOT NULL   
    )
    """)
    
    conn.commit()
    conn.close()


def usthad_registration():

    data = request.json

    conn = sqlite3.connect("mahall.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM usthad
        WHERE aadhaar_number = ?
        """, (
            data.get("aadhaar_number"),
        ))
        
    existing_aadhaar = cursor.fetchone()

    if existing_aadhaar :
        conn.close()
        return jsonify({
        "message": "Aadhaar number already exists"
        })
    
    cursor.execute("""
      SELECT employee_id
      FROM usthad
      ORDER BY id DESC
      LIMIT 1            
      """)
        
    last_employee = cursor.fetchone()

    if last_employee:
            number = last_employee[0][3:]
            number = int(number)
            number += 1
            number = str(number).zfill(4)
            employee_id = "UST" + number
    else:
            employee_id = "UST0001"

    basic_salary = float(data.get("basic_salary",0))
    allowance = float(data.get("allowance",0))
    deduction = float(data.get("deduction",0))

    net_salary = basic_salary + allowance - deduction

    cursor.execute("""
               INSERT INTO usthad(
               full_name,
               photo,
               phone,
               address,
               aadhaar_number,
               date_of_birth,
               gender,
               education,
               islamic_education,
                   
               employee_id,
               position,
               mahall_role,
               date_of_joining,
               employment_status,
            
               basic_salary,
               allowance,
               deduction,
               net_salary       
               )   
               VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                  
            """,(
                data.get("full_name"),
                data.get("photo"),
                data.get("phone"),
                data.get("address"),
                data.get("aadhaar_number"),
                data.get("date_of_birth"),
                data.get("gender"),
                data.get("education"),
                data.get("islamic_education"),
                employee_id,
                data.get("position"),
                data.get("mahall_role"),
                data.get("date_of_joining"),
                data.get("employment_status"),
                basic_salary,
                allowance,
                deduction,
                net_salary ))
  
    conn.commit()
    conn.close()

    return jsonify({
        "message" : "Saved Data"
    })

#Temporary
def view_usthad_list():

    conn = sqlite3.connect("mahall.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id,
        employee_id,
        full_name,
        employment_status
    FROM usthad 
    """)

    usthads = cursor.fetchall()

    conn.close()

    return jsonify(usthads)

def view_usthad_details(id):

    conn = sqlite3.connect("mahall.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM usthad
        WHERE id = ?  
        """, (id,))
    
    usthad = cursor.fetchone()

    conn.close()

    if usthad:
         return jsonify(usthad)
    else:
         return jsonify({
              "message" : "Usthad not Found"
         })

def search_usthad(search_value):
     
     conn = sqlite3.connect("mahall.db")
     cursor = conn.cursor()

     cursor.execute("""
        SELECT id,
        employee_id,
        full_name,
        employment_status FROM usthad 
        WHERE employee_id = ?
        OR full_name = ?
        OR aadhaar_number = ?
        OR employment_status = ?
    """, 
        (search_value,search_value,search_value,search_value))
     
     usthads = cursor.fetchall()

     conn.close()

     if usthads:
          return jsonify(usthads)
     else:
          return jsonify({
               "message" : "Usthad Not Found"
          })
     
def update_usthad():
     
     data = request.json

     conn = sqlite3.connect("mahall.db")
     cursor = conn.cursor()

     cursor.execute("""
        SELECT * FROM usthad
        WHERE aadhaar_number = ?
        AND id != ? 
        """,(
             data.get("aadhaar_number"),
             data.get("id")
        ) )
     existing_aadhaar = cursor.fetchone()

     if existing_aadhaar:
          conn.close()
          return jsonify({
               "message" : "Aadhaar Already Exists"
          })
     else:
          basic_salary = float(data.get("basic_salary"))
          allowance = float(data.get("allowance"))
          deduction = float(data.get("deduction"))
          net_salary = basic_salary + allowance - deduction
          
          cursor.execute("""
         UPDATE usthad 
         SET 
            full_name = ?,
            photo = ?,
            phone = ?,
            address = ?,
            aadhaar_number = ?,
            date_of_birth = ?,
            gender = ?,
            education = ?,
            islamic_education = ?,
                   
            employee_id = ?,
            position = ?,
            mahall_role = ?,
            date_of_joining = ?,
            employment_status = ?,
            
            basic_salary = ?,
            allowance = ?,
            deduction = ?,
            net_salary = ?
         WHERE id = ? 
         """, (
                data.get("full_name"),
                data.get("photo"),
                data.get("phone"),
                data.get("address"),
                data.get("aadhaar_number"),
                data.get("date_of_birth"),
                data.get("gender"),
                data.get("education"),
                data.get("islamic_education"),
                data.get("employee_id"),
                data.get("position"),
                data.get("mahall_role"),
                data.get("date_of_joining"),
                data.get("employment_status"),
                basic_salary,
                allowance,
                deduction,
                net_salary,
                data.get("id")))
     
     conn.commit()
     conn.close()

     return jsonify({
          "message" : "Updated Successfully"
     })

def delete_usthad():
     
     data = request.json

     conn = sqlite3.connect("mahall.db")
     cursor = conn.cursor()

     cursor.execute("""
        SELECT id FROM usthad
        WHERE id = ?
        """,(
             data.get("id"),
        ))
     existing_usthad = cursor.fetchone()

     if existing_usthad:
          cursor.execute("""
            DELETE FROM usthad
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
               "message" : "Usthad Not Found"
          })
          
     
                