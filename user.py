import sqlite3
from flask import request, jsonify

def init_users_table_db():

    conn = sqlite3.connect("mahall.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        
        username TEXT NOT NULL UNIQUE,
            
        password TEXT NOT NULL,
                   
        role TEXT NOT NULL )
                   
    """)

    conn.commit()
    conn.close()

def create_user():

    data = request.json

    conn = sqlite3.connect("mahall.db")
    cursor = conn.cursor()

    cursor.execute("""
                   
      SELECT * FROM users
                   
      WHERE username = ?
        
      """,(
          data.get("username"),
      ))
    
    user = cursor.fetchone()

    if user:
        conn.close()
        return jsonify({
            "Message" : "Username Already Exists"
        })
    else:
        cursor.execute("""
      INSERT INTO users(
      
      username, 
      password,
      role)
                   
      VALUES(?,?,?)
    
    """,(
        data.get("username"),
        data.get("password"),
        data.get("role")
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "Message" : "User Created Successfully"
    })

def login():

    data = request.json

    conn = sqlite3.connect("mahall.db")    
    cursor = conn.cursor()

    cursor.execute("""
               
    SELECT * FROM users
    
    WHERE username = ? AND
    password = ?   
    
    """,(
        data.get("username"),
        data.get("password")
    ))

    user = cursor.fetchone()

    conn.close()

    if user :
        
        return jsonify({
            "Message" : "Access Granted"
        })
    else:
        return jsonify({
            "Message" : "Incorrect Username or Password"
        })

def forgot_password():

    data = request.json

    conn = sqlite3.connect("mahall.db")
    cursor = conn.cursor()

    cursor.execute("""
      UPDATE users
                   
      SET
            password = ?

      WHERE 
            username = ?            
 """,
    (
        data.get("password"),
        data.get("username")
    ))

    cursor.rowcount
    
    conn.commit()
    conn.close()

    return jsonify({
        "Message" : "Password Changed Successfully"
    })
