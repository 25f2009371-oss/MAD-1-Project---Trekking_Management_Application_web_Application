from flask import Flask,render_template
from models import db


app=None
def setup_app():
    global app
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///databse.sqlite3"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    print("Database setup done ...... ")
    app.app_context().push()
setup_app()


app_dict = [
    {
        "t_treks": 10,
        "t_users": 100,
        "t_staffs": 12,
        "t_booking": 8   # singular key to match template
    }
]
app_data = [
    {"b_id": "B001", "uname": "Amit Sharma", "camp": "Everest base camp", "b_date": "12 August 2026", "status": "Booked"},
    {"b_id": "B002", "uname": "Amia", "camp": "East base camp", "b_date": "14 August 2026", "status": "Booked"},
    {"b_id": "B003", "uname": "Narma Ga", "camp": "Kedarnath trek", "b_date": "1 July 2026", "status": "Cancelled"}
]
trekdata = [
    {"id": 1, "trekname": "Everest Base Camp", "location": "Nepal", "difficulty": "Hard", "slots": 20, "status": "Open"},
    {"id": 2, "trekname": "Kedarnath Trek", "location": "India", "difficulty": "Medium", "slots": 15, "status": "Open"},
    {"id": 3, "trekname": "Valley of Flowers", "location": "India", "difficulty": "Easy", "slots": 30, "status": "Closed"},
]

dct=[

        {"sid": 1, "name": "Amit Sharma", "email": "amit@example.com", "contact": "9876543210", "status": "Pending"},
    {"sid": 2, "name": "Priya Verma", "email": "priya@example.com", "contact": "9123456780", "status": "Approved"},
    {"sid": 3, "name": "Rahul Singh", "email": "rahul@example.com", "contact": "9988776655", "status": "Rejected"},
]

@app.route("/admin_dashboard.html")
def admin_dashboard():
    return render_template("admin_dashboard.html", app_dict=app_dict,app_data=app_data)

@app.route("/manage_treks.html")
def managetrek():
    return render_template("manage_treks.html",trekdata=trekdata)


@app.route("/all_staff.html")
def staff():
    return render_template("all_staff.html",dct=dct)

@app.route("/all_users.html")
def user_mng():
    return render_template("all_users.html")


@app.route("/Bookings.html")
def bkng_admin():
    return render_template("Bookings.html")



if __name__ == "__main__":
    app.run(debug=True)
