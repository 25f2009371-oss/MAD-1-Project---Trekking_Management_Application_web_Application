from flask import Flask,render_template,request,redirect,url_for
from models import db,User



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




@app.route('/login/', methods=["GET", "POST"])
@app.route('/logout', methods=["GET", "POST"])
@app.route('/', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        uname = request.form.get("emailid")
        pwd = request.form.get("pwd")        
        user = db.session.query(User).filter(User.email == uname, User.password == pwd).first()
        if user and str(user.role) == "0":
            return redirect(url_for('admin'))
        else:
            return redirect(url_for("register"))

    return render_template('login.html')


@app.route('/register', methods=['GET','POST'])
def register():
    return render_template('register.html')


@app.route('/admin_dashboard')
def admin():
    return render_template("admin_dashboard.html")



@app.route('/manage_treks')
def manageadmin():
    return render_template("manage_treks.html")

@app.route("/add_edit_trek")
def add_edit_trek():
    return render_template("add_edit_trek.html")


@app.route('/all_staffs')
def admin_staff():
    return render_template("all_staff.html")



@app.route('/all_users')
def admin_user():
    return render_template("all_users.html")

@app.route('/bookings')
def admin_bookings():
    return render_template("Bookings.html")



@app.route('/staff_dashboard')
def staff():
    return render_template("staff_dashboard.html")



@app.route('/staff_trek_manage')
def staff_trek_manage():
    return render_template("staff_trek_manage.html")


@app.route('/participants')
def staff_participants():
    return render_template("participants.html")

@app.route('/profile_staff')
def staff_profile():
    return render_template("profile_staff.html")



@app.route('/trekker_dashboard')
def trekker():
    return render_template("trekker_dashboard.html")


@app.route('/all_treks')
def trekker_treks():
    return render_template("all_treks.html")



@app.route('/my_bookings')
def trekker_bookings():
    return render_template("my_bookings.html")



@app.route('/profile_trekker')
def profile_trekker():
    return render_template("profile_trekker.html")




if __name__ == "__main__":
    app.run(debug=True)
