import webview
from flask import Flask, jsonify, request
import threading
import sqlite3

from user import (
    init_users_table_db,
    create_user,
    login
)

from member import (
    init_member_db,
    save_member_registration,
    save_family_member,
    view_members,
    view_family_members,
    search_member,
    update_member,
    update_family_member,
    delete_member,
    delete_family_member
)


def init_db():
    conn = sqlite3.connect("mahall.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS registrations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        groom_fname TEXT,
        groom_lname TEXT,
        groom_mobile TEXT
    )
    """)

    conn.commit()
    conn.close()

app = Flask(__name__, static_folder='web', template_folder='web')

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/api/hello', methods=['POST'])
def hello():
    data = request.json
    name = data.get('name', 'World')
    return jsonify({"message": f"Hello {name} from Python!"})


@app.route('/api/add', methods=['POST'])
def add():
    data = request.json
    a = data.get('a', 'World')
    b = data.get('b', 'World')
    sum = a + b
    return jsonify({"result": f"sum is {sum}"})

#Login Route
@app.route("/api/create_user", methods=["POST"])
def create_user_route():
    return create_user()

@app.route("/api/login")
def login_route():
    return login()
    
@app.route('/api/save_registration', methods=['POST'])
def save_registration():

    data = request.json

    groom_fname = data.get('groom_fname')
    groom_lname = data.get('groom_lname')
    groom_mobile = data.get('groom_mobile')

    conn = sqlite3.connect("mahall.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO registrations
    (groom_fname, groom_lname, groom_mobile)
    VALUES (?, ?, ?)
    """, (groom_fname, groom_lname, groom_mobile))

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Registration saved successfully"
    })


@app.route('/api/view')
def view():

    conn = sqlite3.connect("mahall.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM registrations")

    rows = cursor.fetchall()

    conn.close()

    return jsonify(rows)


@app.route('/view')
def view_page():
    return app.send_static_file('view.html')


@app.route("/member_registration")
def member_registration():
    return app.send_static_file("member_registration.html")

@app.route("/api/save_family_member", methods=["POST"])
def save_family_member_route():
    return save_family_member()

@app.route('/api/search/<groom_fname>')
def search(groom_fname):

    print("Searching for:", groom_fname)

    conn = sqlite3.connect("mahall.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM registrations WHERE groom_fname = ?",
        (groom_fname,)
    )

    row = cursor.fetchone()

    print("Found;", row)

    conn.close()

    return jsonify(row)


@app.route("/api/save_member", methods=["POST"])
def save_member():
    return save_member_registration()

@app.route("/family_members")
def family_members():
    return app.send_static_file("family_members.html")

@app.route("/api/view_members")
def view_members_route():
    return view_members()

@app.route("/api/view_family_members")
def view_family_members_route():
    return view_family_members()

#search member
@app.route("/api/search_member/<search_value>")
def search_member_route(search_value):
    return search_member(search_value)

#update Member
@app.route("/api/update_member" , methods=["PUT"])
def update_member_route():
    return update_member()

@app.route("/api/update_family_member" , methods=["PUT"])
def update_family_member_route():
    return update_family_member()

@app.route("/api/delete_member" , methods=["DELETE"])
def delete_member_route():
    return delete_member()

@app.route("/api/delete_family_member" , methods=["DELETE"])
def delete_family_member_route():
    return delete_family_member()

def start_flask():
    app.run(port=5000, threaded=True)

if __name__ == '__main__':

    init_db()

    init_member_db()

    init_users_table_db()
    
    # Start Flask in background
    threading.Thread(target=start_flask, daemon=True).start()
    
    # Create window
    window = webview.create_window(
        'My Awesome App',
        'http://127.0.0.1:5000',
        width=1024,
        height=768,
        resizable=True
    )
    webview.start()
