from flask import Flask,render_template,request,redirect,url_for
from models import db, User, Trek, Booking
from datetime import datetime

def get_all_staffs():
    stff_data = db.session.query(User).filter(User.role == "1").all() 
    return stff_data

def get_admin_dashboard_stats():
    total_treks = db.session.query(Trek).count()
    total_users = db.session.query(User).filter(User.role == "2").count() 
    total_staff = db.session.query(User).filter(User.role == "1").count() 
    total_bookings = db.session.query(Booking).count()
    stats = [{
        "t_treks": total_treks,
        "t_users": total_users,
        "t_staffs": total_staff,
        "t_booking": total_bookings}]
    return stats

def get_trek_data():
    all_treks = db.session.query(Trek).all()
    return all_treks


def get_all_bookings():
    bookings_data = db.session.query(
        Booking.booking_id,
        User.full_name,
        Booking.trek_id,
        Booking.booking_date,
        Booking.status
    ).join(User, Booking.user_id == User.user_id).order_by(Booking.booking_id.desc()).all()
    return bookings_data


def get_all_registered_data():
    user_data = db.session.query(User).filter(User.role == 2).all()
    return user_data

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
        user = db.session.query(User).filter(User.email == uname).first()
        if user and str(user.role) == "0":
            return redirect(url_for('admin'))

        elif user and str(user.role)=="1":
            return redirect(url_for('staff'))

        elif user and str(user.role)=="2":
                    return redirect(url_for('trekker'))

        else:
            return redirect(url_for("register"))

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        uname = request.form.get("emailid")
        pwd = request.form.get("pwd")
        role = request.form.get("utype")
        user = db.session.query(User).filter(User.email == uname).first()
        if user:
            return render_template("register.html", err_msg="Sorry, email is already used, use another email")
        else:
            name = request.form.get("nam")
            phone = request.form.get("phn")
            
            initial_status = "Pending" if str(role) == "1" else "Active"
            uc = User(email=uname, password=pwd, role=role, full_name=name, phone=phone, status=initial_status)
            
            db.session.add(uc)
            db.session.commit() 
            return redirect(url_for('login')) 

    return render_template('register.html')

@app.route('/admin_dashboard')
def admin():
    data1=get_admin_dashboard_stats()
    data2=get_all_bookings()
    return render_template("admin_dashboard.html", r_data=data2, app_dict=data1)

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    user = db.session.query(User).first()    
    if request.method == "POST":
        user.full_name = request.form.get("nam")
        user.password = request.form.get("pwd")
        user.phone = request.form.get("phn")
        db.session.commit()
        return redirect(url_for('profile_trekker'))

    return render_template('edit_profile.html', d=user)

@app.route('/manage_treks')
def manageadmin():
    data3=get_trek_data()
    return render_template("manage_treks.html",trekdata=data3)

@app.route("/add_edit_trek", methods=['GET', 'POST'])
def add_edit_trek():
    if request.method == 'POST':
        t_name = request.form.get("trek_name")
        t_location = request.form.get("location")
        t_difficulty = request.form.get("difficulty")
        t_duration = request.form.get("duration")
        slots = int(request.form.get("available_slots") or 10)
        s_date = datetime.strptime(request.form.get("start_date"), '%Y-%m-%d').date()
        e_date = datetime.strptime(request.form.get("end_date"), '%Y-%m-%d').date()
        t_status = request.form.get("status")
        t_desc = request.form.get("description")
        
        staff_id = request.form.get("assigned_staff_id")
        staff_id = int(staff_id) if staff_id and staff_id != "None" else None

        new_trek = Trek(
            trek_name=t_name,
            location=t_location,
            difficulty=t_difficulty,
            duration=t_duration,
            start_date=s_date,
            end_date=e_date,
            total_slots=slots,
            available_slots=slots, 
            status=t_status,
            description=t_desc,
            assigned_staff_id=staff_id
        )
        db.session.add(new_trek)
        db.session.commit()
        return redirect(url_for('manageadmin'))
        
    staff_members = db.session.query(User).filter(User.role == "1").all()
    return render_template("add_edit_trek.html", staff_list=staff_members)


@app.route('/all_staffs')
def admin_staff():
    active_staff = db.session.query(User).filter(User.role == "1", User.status == "Active").all()    
    pending_staff = db.session.query(User).filter(User.role == "1", User.status == "Pending").all()
    return render_template("all_staff.html", current_staff=active_staff, pending_staff=pending_staff)


@app.route('/all_users')
def admin_user():
    data2 = get_all_registered_data() 
    return render_template("all_users.html", trkkdata=data2)

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
    data = get_trek_data() 
    return render_template("all_treks.html", trekdata=data)



@app.route('/my_bookings')
def trekker_bookings():
    current_user = db.session.query(User).filter(User.role == "2").first()    
    my_b = db.session.query(Booking, Trek).join(Trek, Booking.trek_id == Trek.trek_id).filter(Booking.user_id == current_user.user_id).all()
    return render_template("my_bookings.html", bookings=my_b)


@app.route('/profile_trekker')
def profile_trekker():
    return render_template("profile_trekker.html")


@app.route('/update_status/<int:uid>/<new_status>')
def update_status(uid, new_status):
    user_to_update = db.session.query(User).filter(User.user_id == uid).first()
    if user_to_update:
        user_to_update.status = new_status
        db.session.commit()
        if str(user_to_update.role) == "1":
            return redirect(url_for('admin_staff'))
        else:
            return redirect(url_for('admin_user'))
    return redirect(url_for('admin'))

@app.route('/delete_trek/<int:trek_id>')
def delete_trek(trek_id):
    trek_to_delete = db.session.query(Trek).filter(Trek.trek_id == trek_id).first()    
    if trek_to_delete:
        db.session.delete(trek_to_delete)
        db.session.commit()
    return redirect(url_for('manageadmin'))



@app.route('/book_trek/<int:trek_id>')
def book_trek(trek_id):
    trek_to_book = db.session.query(Trek).filter(Trek.trek_id == trek_id).first()    
    current_user = db.session.query(User).filter(User.role == "2").first()
    if trek_to_book and trek_to_book.available_slots > 0:
        trek_to_book.available_slots -= 1
        new_booking = Booking(
            user_id=current_user.user_id, 
            trek_id=trek_to_book.trek_id, 
            booking_date=datetime.now().date(), 
            status="Confirmed")
        db.session.add(new_booking)
        db.session.commit()
    return redirect(url_for('trekker_bookings'))

if __name__ == "__main__":
    app.run(debug=True)
