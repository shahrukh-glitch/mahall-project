import sqlite3
from flask import request, jsonify
from datetime import date

def init_salary_history_db():

    conn = sqlite3.connect("mahall.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS salary_history(
    
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usthad_id INTEGER NOT NULL ,
    employee_id TEXT NOT NULL,
    full_name TEXT NOT NULL,
        
        month INTEGER NOT NULL,
        year INTEGER NOT NULL,
            
            basic_salary REAL NOT NULL,
            allowance REAL NOT NULL DEFAULT 0,
            deduction REAL NOT NULL DEFAULT 0,
            net_salary REAL NOT NULL,
                
                payment_date TEXT ,
                payment_status TEXT NOT NULL DEFAULT 'Pending',

                   FOREIGN KEY (usthad_id) REFERENCES usthad(id)              
    ) 
    """)
    
    conn.commit()
    conn.close()

def generate_payroll():

    data = request.json
    
    conn = sqlite3.connect("mahall.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM salary_history
        WHERE month = ? AND year = ?   
        """,(
            data.get("month"),
            data.get("year")
        ))

    existing_payroll = cursor.fetchone()

    if existing_payroll:
        conn.close()
        return jsonify({
            "message" : "Payroll Already Exists"
        })
    else:
        cursor.execute("""
            SELECT id,
                employee_id,
                full_name,
                basic_salary,
                allowance,
                deduction,
                net_salary  
            FROM usthad 
            WHERE employment_status = 'Active'
             """)
        active_usthads = cursor.fetchall()

        if  not active_usthads:
            conn.close()
            return jsonify({
                "message" : "No Active Usthads Found"
            })


        for usthad in active_usthads:
            usthad_id = usthad[0]
            employee_id = usthad[1]
            full_name = usthad[2]
            basic_salary = usthad[3]
            allowance = usthad[4]
            deduction = usthad[5]
            net_salary = usthad[6]
        
            cursor.execute("""
            INSERT INTO salary_history(
            usthad_id,
            employee_id,
            full_name,
            month,
            year,
            basic_salary,
            allowance,
            deduction,
            net_salary,
            payment_date,
            payment_status   
            )
            VALUES (?,?,?,?,?,?,?,?,?,?,?)           
            """,(
                usthad_id,
                employee_id,
                full_name,
                data.get("month"),
                data.get("year"),
                basic_salary,
                allowance,
                deduction,
                net_salary,
                None,
                "Pending"))
       
    conn.commit()
    conn.close()

    return jsonify({
        "message" : "Payroll Generated Successfully"
    })

#Temp
def view_salary_history():
    
    conn = sqlite3.connect("mahall.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM salary_history")

    rows = cursor.fetchall()
    
    conn.close()
    
    return jsonify(rows)

def pay_salary():

    data = request.json

    conn = sqlite3.connect("mahall.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM salary_history
        WHERE id = ? 
        """,(
            data.get("id"),
        ) )
    
    existing_payroll = cursor.fetchone()

    if not existing_payroll:
          conn.close()
          return jsonify({
               "message" : "No Record Found"
          })
    else: 
        payment_status = existing_payroll[11]
        
        if payment_status == "Paid":
            conn.close()
            return jsonify({
                "message" : "Already Paid"
            })
        else:
            today = date.today()
            cursor.execute("""
                UPDATE salary_history
                SET payment_date = ?,
                    payment_status = ?
                WHERE id = ?   
                """,(
                    today,
                    "Paid",
                    data.get("id")
                ))
            conn.commit()
            conn.close()

            return jsonify({
                "message" : "Paid Successfully"
            })
        
def generate_payslip():

    data = request.json

    conn = sqlite3.connect("mahall.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM salary_history
        WHERE id = ?
        """,(
            data.get("id"),
        ))
    rows = cursor.fetchone()

    conn.close()
    
    if not rows:
            return jsonify({
                "message": "Payslip Not Found"
            })
    
    payment_status = rows[11]
    if payment_status != "Paid":
            return jsonify({
                "message": "Salary Not Paid Yet"
            })
    return jsonify(rows)

def search_payslip():

    data = request.json
     
    conn = sqlite3.connect("mahall.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM salary_history
        WHERE employee_id = ?
        AND month = ?
        AND year = ?    
        """,(
             data.get("employee_id"),
             data.get("month"),
             data.get("year")
        )
        )
    payslip = cursor.fetchone()

    conn.close()

    if payslip:
         payment_status = payslip[11]
         if payment_status != "Paid":
              return jsonify ({
                   "message" : "Salary Not Paid Yet"
              })
         else:
              return jsonify(payslip)
    else:
         return jsonify({
              "message" : "Payslip Not Found"
         })
         
    



         

  
 

    


            


    