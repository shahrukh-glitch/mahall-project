import sqlite3
from flask import request, jsonify
import bcrypt

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
        hashed_password = bcrypt.hashpw(
            data.get("password").encode(),
            bcrypt.gensalt())

        cursor.execute("""
        INSERT INTO users(
      
        username, 
        password,
        role)
                   
        VALUES(?,?,?)
    
        """,(
          data.get("username"),
          hashed_password.decode(),
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
    
    WHERE username = ?   
    
    """,(
        data.get("username"),
    ))

    user = cursor.fetchone()
    conn.close()

    if user:
        if bcrypt.checkpw(
            data.get("password").encode(),
            user[2].encode()
        ):
            return jsonify({
                "message" : "Access Granted"
            })
        else:
            return jsonify({
                "message" : "Incorrect Password"
            })
    else:
        return jsonify({
            "message" : "User not Found"
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

#temporary function for testing.
def view_users():

    conn = sqlite3.connect("mahall.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM users
    """)

    users = cursor.fetchall()

    conn.close()

    return jsonify(users)
    
    
