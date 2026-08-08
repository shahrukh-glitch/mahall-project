import webview
from flask import Flask, jsonify, request
import threading
import sqlite3

from user import (
    init_users_table_db,
    create_user,
    login,
    view_users
)

from member import (
    init_member_db,
    save_member_registration,
    save_family_member,
    view_members,
    view_family_members,
    search_member,
    search_member_by_id,
    search_family_member,
    update_member,
    update_family_member,
    delete_member,
    delete_family_member
)

from usthad import (
    init_usthad_db,
    usthad_registration,
    view_usthad_list,
    view_usthad_details,
    search_usthad,
    update_usthad,
    delete_usthad
)

from payroll import(
    init_salary_history_db,
    generate_payroll,
    view_salary_history,
    pay_salary,
    generate_payslip,
    search_payslip
)

from donation import(
    init_donation_db,
    save_donation,
    view_donations,
    search_donation,
    update_donation,
    delete_donation
    )

from expense import(
    init_expense_db,
    save_expense,
    view_expense,
    search_expense,
    update_expense,
    delete_expense
)

from dashboard import(
    dashboard
)

from cash_register import(
    init_cash_register_db,
    view_cash_register
)

from reports import(
    donation_reports,
    expense_reports,
    financial_summary
)

from ledger import(
    ledger,
    cash_flow
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
def login_page():
    return app.send_static_file('login.html')

@app.route("/dashboard")
def dashboard_page():
    return app.send_static_file("dashboards.html")

@app.route("/member_registration")
def member_registration():
    return app.send_static_file("member_registration.html")

@app.route("/donation")
def donation_page():
    return app.send_static_file("donation.html")

@app.route("/expense")
def expense_page():
    return app.send_static_file("expense.html")

@app.route("/salary")
def salary_page():
    return app.send_static_file("payroll.html")

@app.route("/cash_register")
def cash_register_page():
    return app.send_static_file("cash_register.html")

@app.route("/reports")
def reports_page():
    return app.send_static_file("reports.html")

#  LOGIN

@app.route("/api/create_user", methods=["POST"])
def create_user_route():
    return create_user()

@app.route("/api/login",methods = ["POST"])
def login_route():
    return login()

@app.route("/api/view_users", methods=["GET"])
def view_users_route():
    return view_users()

# MEMBER REGISTRATION   

@app.route("/api/save_family_member", methods=["POST"])
def save_family_member_route():
    return save_family_member()

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

@app.route("/api/search_member/<search_value>")
def search_member_route(search_value):
    return search_member(search_value)

@app.route("/api/search_family_member/<int:member_id>")
def search_family_member_route(member_id):
    return search_family_member(member_id)

@app.route("/api/search_member_by_id/<int:member_id>")
def search_member_by_id_route(member_id):
    return search_member_by_id(member_id)

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

#    Usthad Registration

@app.route("/api/usthad_registration", methods = ["POST"])
def usthad_registration_route():
    return usthad_registration()

@app.route("/api/view_usthad_list", methods=["GET"])
def view_usthad_list_route():
    return view_usthad_list()

@app.route("/api/view_usthad/<int:id>")
def view_usthad_details_route(id):
    return view_usthad_details(id)

@app.route("/api/search_usthad/<search_value>")
def search_usthad_route(search_value):
    return search_usthad(search_value)

@app.route("/api/update_usthad", methods = ["PUT"])
def update_usthad_route():
    return update_usthad()

@app.route("/api/delete_usthad", methods = ["DELETE"])
def delete_usthad_route():
    return delete_usthad()

#    PAYROLL

@app.route("/api/generate_payroll", methods = ["POST"])
def generate_payroll_route():
    return generate_payroll()

@app.route("/api/view_salary_history")
def view_salary_history_route():
    return view_salary_history()

@app.route("/api/pay_salary", methods = ["PUT"])
def pay_salary_route():
    return pay_salary()

@app.route("/api/generate_payslip",methods = ["POST"])
def generate_payslip_route():
    return generate_payslip()

@app.route("/api/search_payslip", methods = ["POST"])
def search_payslip_route():
    return search_payslip()

#  DONATION

@app.route("/api/save_donation", methods = ["POST"])
def save_donation_route():
    return save_donation()

@app.route("/api/view_donations")
def view_donations_route():
    return view_donations()

@app.route("/api/search_donation/<search_value>")
def search_donation_route(search_value):
    return search_donation(search_value)

@app.route("/api/update_donation", methods = ["PUT"])
def update_donation_route():
    return update_donation()

@app.route("/api/delete_donation", methods = ["DELETE"])
def delete_donation_route():
    return delete_donation()

# EXPENSE

@app.route("/api/save_expense",methods = ["POST"])
def save_expense_route():
    return save_expense()

@app.route("/api/view_expense")
def view_expense_route():
    return view_expense()

@app.route("/api/search_expense/<search_value>")
def search_expense_route(search_value):
    return search_expense(search_value)

@app.route("/api/update_expense",methods = ["PUT"])
def update_expense_route():
    return update_expense()

@app.route("/api/delete_expense",methods = ["DELETE"])
def delete_expense_route():
    return delete_expense()

#    Dashboard

@app.route("/api/dashboard")
def dashboard_route():
    return dashboard()

#    Cash Register

@app.route("/api/view_cash_register", methods=["GET"])
def view_cash_register_api():
    return view_cash_register()

#    Reports

@app.route("/api/donation_reports",methods = ["POST"])
def donation_reports_route():
    return donation_reports()

@app.route("/api/expense_reports",methods = ["POST"])
def expense_reports_route():
    return expense_reports()

@app.route("/api/financial_summary",methods = ["POST"])
def financial_summary_route():
    return financial_summary()

#     Ledger

@app.route("/api/ledger", methods = ["POST"])
def ledger_route():
    return ledger()

@app.route("/api/cash_flow", methods = ["POST"])
def cash_flow_route():
    return cash_flow()

def start_flask():
    app.run(port=5000, threaded=True)

if __name__ == '__main__':

    init_db()

    init_member_db()

    init_users_table_db()

    init_usthad_db()

    init_salary_history_db()

    init_donation_db()

    init_expense_db()

    init_cash_register_db()
    
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
