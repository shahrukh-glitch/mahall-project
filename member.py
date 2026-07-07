import sqlite3
from flask import request, jsonify


# Create Member Registration Table
def init_member_db():

    conn = sqlite3.connect("mahall.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS member_registration (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        registration_number TEXT,
        mahallu TEXT,
        ward TEXT,
        house_number TEXT,
        family_number TEXT,
        registration_date TEXT,

        family_head TEXT,
        father_name TEXT,
        house_name TEXT,
        phone TEXT,
        address TEXT

    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS family_members (
       
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        family_id INTEGER,

        member_name TEXT,
        gender TEXT,
        age INTEGER,
        relationship TEXT,
        occupation TEXT,
        education TEXT,

        FOREIGN KEY (family_id)
        REFERENCES member_registration(id)

    )
    """)



    conn.commit()
    conn.close()


# Save Member Registration
def save_member_registration():

    data = request.json

    conn = sqlite3.connect("mahall.db")
    cursor = conn.cursor()

    cursor.execute("""

        INSERT INTO member_registration(

            registration_number,
            mahallu,
            ward,
            house_number,
            family_number,
            registration_date,

            family_head,
            father_name,
            house_name,
            phone,
            address

        )

        VALUES(?,?,?,?,?,?,?,?,?,?,?)

    """,

    (

        data.get("registration_number"),
        data.get("mahallu"),
        data.get("ward"),
        data.get("house_number"),
        data.get("family_number"),
        data.get("registration_date"),

        data.get("family_head"),
        data.get("father_name"),
        data.get("house_name"),
        data.get("phone"),
        data.get("address")

    ))
    member_id = cursor.lastrowid
    conn.commit()

    conn.close()

    return jsonify({
        "message": "Member Registration Saved Successfully",
        "family_id" : member_id
    })

def save_family_member():

    data = request.json

    conn = sqlite3.connect("mahall.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO family_members(

            family_id,
            member_name,
            gender,
            age,
            relationship,
            occupation,
            education

        )

        VALUES(?,?,?,?,?,?,?)

    """, (

        data["family_id"],
        data["member_name"],
        data["gender"],
        data["age"],
        data["relationship"],
        data["occupation"],
        data["education"]

    ))

    
    conn.commit()
    conn.close()

    return jsonify({
        "message": "Member Saved Successfully"
    })


# View All Families
def view_members():

    conn = sqlite3.connect("mahall.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM member_registration")

    rows = cursor.fetchall()

    conn.close()

    return jsonify(rows)

#View All Family Members
def view_family_members():

    conn = sqlite3.connect("mahall.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM family_members ")

    rows = cursor.fetchall()

    conn.close()

    return jsonify(rows)


# Search by Registration Number
def search_member(search_value):

    conn = sqlite3.connect("mahall.db")
    cursor = conn.cursor()

    cursor.execute("""

        SELECT *

        FROM member_registration

        WHERE registration_number = ?

        OR family_head = ?

    """, (search_value, search_value))

    member = cursor.fetchone()


    if member is None:
        conn.close()
        return jsonify(
            "Member Not Found"
        )
    else:
        family_id = member[0]
     
        cursor.execute("""
    
         SELECT *
         
         FROM family_members WHERE family_id = ?
         
    """, (family_id,))

    family_members = cursor.fetchall()

    conn.close()

    return jsonify(
        {
            "member" : 
            member,
            "family_members" : 
            family_members
        }
    )

#Updating Member 
def update_member():

    data = request.json

    conn = sqlite3.connect("mahall.db")
    cursor = conn.cursor()

    cursor.execute("""
    
    UPDATE member_registration
    SET 
            registration_number = ?,
            mahallu = ?,
            ward = ?,
            house_number = ?,
            family_number = ?,
            registration_date = ?,

            family_head = ?,
            father_name = ?,
            house_name = ?,
            phone = ?,
            address = ?

       WHERE id = ?
    
      
    """,
    (data.get("registration_number"),
    data.get("mahallu"),
    data.get("ward"),
    data.get("house_number"),
    data.get("family_number"),
    data.get("registration_date"),

    data.get("family_head"),
    data.get("father_name"),
    data.get("house_name"),
    data.get("phone"),
    data.get("address"),
    data.get("id")))
    
    
    conn.commit()
    conn.close()

    return jsonify({
        
        "message" : "Updated Successfully"
    })

def update_family_member():

    data = request.json

    conn = sqlite3.connect("mahall.db")
    cursor = conn.cursor()

    cursor.execute("""
    
    UPDATE family_members
    SET 
            family_id = ?,
            member_name = ?,
            gender = ?,
            age = ?,
            relationship = ?,
            occupation = ?,
            education = ?

       WHERE id = ?
    
      
    """,
    (data.get("family_id"),
        data.get("member_name"),
        data.get("gender"),
        data.get("age"),
        data.get("relationship"),
        data.get("occupation"),
        data.get("education"),
        data.get("id")))
    
    
    conn.commit()
    conn.close()

    return jsonify({
        
        "message" : "Updated Successfully"
    })

def delete_member():

    data = request.json

    conn = sqlite3.connect("mahall.db")
    cursor = conn.cursor()

    cursor.execute("""
    
     DELETE from family_members

     WHERE family_id = ?

     """,
    ( data.get("id"),))

    cursor.execute("""
     
     DELETE from member_registration

     WHERE id = ?

    """,
    (data.get("id"),))

    conn.commit()
    conn.close()

    return jsonify({
        "message" : "Deleted Successfully"
    })

def delete_family_member():
    
    data = request.json

    conn = sqlite3.connect("mahall.db")
    cursor = conn.cursor()

    cursor.execute("""
    
    DELETE from family_members
    
    WHERE id = ?
    
    """,
    (data.get("id"),))

    conn.commit()
    conn.close()

    return jsonify({
        "message" : "Deleted Successfully"
    })