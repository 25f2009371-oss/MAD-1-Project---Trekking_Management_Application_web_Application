from flask import Flask,render_template
from models import db

app = Flask(__name__)
"""
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
    """

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


@app.route("/admin")
def admin_dashboard():
    return render_template("admin_dashboard.html", app_dict=app_dict,app_data=app_data)

@app.route("/manage-trek")
def managetrek():
    return render_template("manage_treks.html")



if __name__ == "__main__":
    app.run(debug=True)
