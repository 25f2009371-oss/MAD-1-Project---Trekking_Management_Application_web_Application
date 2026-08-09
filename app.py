from flask import Flask, render_template, request, redirect, url_for, session
from models import db, User, Trek, Booking
from datetime import datetime

def get_all_staffs():
    stff_data = db.session.query(User).filter(User.role == "1").all() 
    return stff_data

def get_admin_dashboard_stats():
    total_treks = db.session.query(Trek).count()
    total_users = db.session.query(User).filter(User.role == "2").count() 
    t_staff = db.session.query(User).filter(User.role == "1", User.status == "Active").count()    
    total_bookings = db.session.query(Booking).count()
    stats = [{"t_treks": total_treks,
        "t_users": total_users,
        "t_staffs": t_staff,
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
    user_data = db.session.query(User).filter(User.role == "2").all()
    return user_data

app = None
def setup_app():
    global app
    app = Flask(__name__)
    app.secret_key = "Arohan"  
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///databse.sqlite3"
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"connect_args": {"timeout": 15}}
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    
    with app.app_context():
        db.create_all()  
        
    print("Database setup done successfully ")
    app.app_context().push()
setup_app()

@app.route('/')
def index():
    return render_template("main.html")

@app.route('/logout')
@app.route('/login/', methods=["GET", "POST"])
def login():
    if request.path == '/logout':
        session.clear()
        return redirect(url_for('login'))
        
    if request.method == "POST":
        uname = request.form.get("emailid")
        pwd = request.form.get("pwd")        
        user = db.session.query(User).filter(User.email == uname).first()    
        
        if user and user.password == pwd:
            session['user_id'] = user.user_id
            session['role'] = str(user.role)          
            
            if session['role'] == "0":
                return redirect(url_for('admin'))
            elif session['role'] == "1":
                return redirect(url_for('staff'))
            elif session['role'] == "2":
                return redirect(url_for('trekker'))
        else:
            return render_template("login.html", err_msg="Wrong email or password.")

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
    data1 = get_admin_dashboard_stats()
    data2 = get_all_bookings()
    return render_template("admin_dashboard.html", r_data=data2, app_dict=data1)


@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    user = db.session.query(User).filter(User.user_id == session.get('user_id')).first()    
    if request.method == "POST":
        user.full_name = request.form.get("nam")
        user.password = request.form.get("pwd")
        user.phone = request.form.get("phn")
        db.session.commit()
        return redirect(url_for('profile_trekker'))
    return render_template('edit_profile.html', d=user)


@app.route('/manage_treks', methods=['GET', 'POST'])
def manageadmin():
    search_query = request.form.get("search")
    if search_query:
        data3 = db.session.query(Trek).filter(
            (Trek.trek_name.like(f"%{search_query}%")) | 
            (Trek.location.like(f"%{search_query}%"))
        ).all()
    else:
        data3 = get_trek_data()
    return render_template("manage_treks.html", trekdata=data3)


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
            trek_name=t_name, location=t_location, difficulty=t_difficulty,
            duration=t_duration, start_date=s_date, end_date=e_date,
            total_slots=slots, available_slots=slots, status=t_status,
            description=t_desc, assigned_staff_id=staff_id
        )
        db.session.add(new_trek)
        db.session.commit()
        return redirect(url_for('manageadmin'))
        
    staff_members = db.session.query(User).filter(User.role == "1").all()
    return render_template("add_edit_trek.html", staff_list=staff_members)


@app.route('/all_staffs', methods=['GET', 'POST'])
def admin_staff():
    if request.method == 'POST':
        search_query = request.form.get("search")
        active_staff = db.session.query(User).filter(
            User.role == "1", 
            User.status == "Active",
            (User.full_name.like(f"%{search_query}%")) | 
            (User.email.like(f"%{search_query}%"))
        ).all()    
        
        pending_staff = db.session.query(User).filter(
            User.role == "1", 
            User.status == "Pending",
            (User.full_name.like(f"%{search_query}%")) | 
            (User.email.like(f"%{search_query}%"))
        ).all()
        
    else:
        active_staff = db.session.query(User).filter(User.role == "1", User.status == "Active").all()    
        pending_staff = db.session.query(User).filter(User.role == "1", User.status == "Pending").all()
        
    return render_template("all_staff.html", current_staff=active_staff, pending_staff=pending_staff)


@app.route('/all_users', methods=['GET', 'POST'])
def admin_user():
    if request.method == 'POST':
        search_query = request.form.get("search")
        data2 = db.session.query(User).filter(
            User.role == "2",
            (User.full_name.like(f"%{search_query}%")) | 
            (User.email.like(f"%{search_query}%"))
        ).all()
    else:
        data2 = get_all_registered_data() 
    return render_template("all_users.html", trkkdata=data2)

@app.route('/bookings', methods=['GET', 'POST'])
def admin_bookings():
    if request.method == 'POST':
        search_query = request.form.get("search")
        all_bookings = db.session.query(Booking, User, Trek)\
            .join(User, Booking.user_id == User.user_id)\
            .join(Trek, Booking.trek_id == Trek.trek_id)\
            .filter(
                (User.full_name.like(f"%{search_query}%")) | 
                (Trek.trek_name.like(f"%{search_query}%"))).all()
    else:
        all_bookings = db.session.query(Booking, User, Trek)\
            .join(User, Booking.user_id == User.user_id)\
            .join(Trek, Booking.trek_id == Trek.trek_id).all()
            
    return render_template("Bookings.html", bkng=all_bookings)


@app.route('/staff_dashboard')
def staff():
    current_staff_id = session.get('user_id')
    my_assigned_treks = db.session.query(Trek).filter(Trek.assigned_staff_id == current_staff_id).all()    
    return render_template("staff_dashboard.html", treks=my_assigned_treks)


@app.route('/staff_trek_manage', methods=['GET', 'POST'])
def staff_trek_manage():
    if session.get('role') != "1":
        return redirect(url_for('login'))
        
    current_staff_id = session.get('user_id')
    if request.method == "POST":
        t_id = request.form.get("trek_id")
        new_slots = request.form.get("available_slots")
        new_status = request.form.get("status")
        trek_to_update = db.session.query(Trek).filter(
            Trek.trek_id == t_id,
            Trek.assigned_staff_id == current_staff_id
            ).first()        
        if trek_to_update:
            trek_to_update.available_slots = int(new_slots)
            trek_to_update.status = new_status
            db.session.commit()
        return redirect(url_for('staff_trek_manage'))
    my_treks = db.session.query(Trek).filter(Trek.assigned_staff_id == current_staff_id).all()
    trek_ids = [t.trek_id for t in my_treks]
    if trek_ids:
        participants = db.session.query(Booking, User)\
            .join(User, Booking.user_id == User.user_id)\
            .filter(Booking.trek_id.in_(trek_ids)).all()
    else:
        participants = []

    return render_template("staff_trek_manage.html", treks=my_treks, participants=participants)


@app.route('/participants')
def staff_participants():
    if session.get('role') != "1":
        return redirect(url_for('login'))
    current_staff_id = session.get('user_id')
    my_treks = db.session.query(Trek).filter(Trek.assigned_staff_id == current_staff_id).all()
    trek_ids = [t.trek_id for t in my_treks]
    if trek_ids:
        participants_data = db.session.query(Booking, User)\
            .join(User, Booking.user_id == User.user_id)\
            .filter(Booking.trek_id.in_(trek_ids)).all()
    else:
        participants_data = []
    return render_template("participants.html", treks=my_treks, participants=participants_data)


@app.route('/profile_staff')
def staff_profile():
    current_user_id = session.get('user_id')
    staff_info = db.session.query(User).filter(User.user_id == current_user_id).first()
    return render_template("profile_staff.html", d=staff_info)

@app.route('/trekker_dashboard')
def trekker():
    current_user_id = session.get('user_id')
    available_treks = db.session.query(Trek).filter(
        Trek.status == "Open", 
        Trek.available_slots > 0
    ).all()
    my_bookings = db.session.query(Booking, Trek)\
        .join(Trek, Booking.trek_id == Trek.trek_id)\
        .filter(Booking.user_id == current_user_id).all()
    return render_template("trekker_dashboard.html", treks=available_treks, bookings=my_bookings)


@app.route('/all_treks', methods=['GET', 'POST'])
def trekker_treks():
    if request.method == 'POST':
        search_query = request.form.get("search")
        data = db.session.query(Trek).filter((Trek.trek_name.like(f"%{search_query}%")) | 
            (Trek.location.like(f"%{search_query}%"))
        ).all()
    else:
        data = get_trek_data() 
    return render_template("all_treks.html", trekdata=data)

@app.route('/my_bookings')
def trekker_bookings():
    current_user_id = session.get('user_id')    
    my_b = db.session.query(Booking, Trek).join(Trek, Booking.trek_id == Trek.trek_id).filter(Booking.user_id == current_user_id).all()
    return render_template("my_bookings.html", bookings=my_b)


@app.route('/profile_trekker')
def profile_trekker():
    current_user_id = session.get('user_id')
    user_info = db.session.query(User).filter(User.user_id == current_user_id).first()
    return render_template("profile_trekker.html", d=user_info)


@app.route('/update_status/<int:uid>/<new_status>')
def update_status(uid, new_status):        
    user_to_update = db.session.query(User).filter(User.user_id == uid).first()    
    if user_to_update:
        if user_to_update.role == "1" and new_status == "Active":
            active_count = db.session.query(User).filter(User.role == "1", User.status == "Active").count()
            if active_count >= 5:
                active_staff = db.session.query(User).filter(User.role == "1", User.status == "Active").all()
                pending_staff = db.session.query(User).filter(User.role == "1", User.status == "Pending").all()
                return render_template("all_staff.html", 
                                       current_staff=active_staff, 
                                       pending_staff=pending_staff, 
                                       err_msg="Staff is full. Remove someone to add another staff.")                                      
        user_to_update.status = new_status
        db.session.commit()
        if user_to_update.role == "1":
            return redirect(url_for('admin_staff'))
        elif user_to_update.role == "2":
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
    current_user_id = session.get('user_id')
    if not current_user_id:
        return redirect(url_for('login'))
        
    current_user = db.session.query(User).filter(User.user_id == current_user_id).first()
    
    if not current_user or current_user.status in ["Deactivated", "Blacklisted"]:
        data = db.session.query(Trek).all()
        return render_template("all_treks.html", trekdata=data, err_msg="You can't book as you are blacklisted.")    
        
    trek_to_book = db.session.query(Trek).filter(Trek.trek_id == trek_id).first()    
    
    if trek_to_book:
        if trek_to_book.available_slots <= 0:
            data = db.session.query(Trek).all()
            return render_template("all_treks.html", trekdata=data, err_msg="Sorry, this trek is completely full!")
            
        elif trek_to_book.status.lower() != "open":
            data = db.session.query(Trek).all()
            return render_template("all_treks.html", trekdata=data, err_msg=f"Sorry, you cannot book this. The current status is '{trek_to_book.status}'.")
            
        else:
            trek_to_book.available_slots -= 1
            new_booking = Booking(user_id=current_user.user_id, 
                trek_id=trek_to_book.trek_id, 
                booking_date=datetime.now().date(), # <-- Removed str() here!
                status="Confirmed")
            db.session.add(new_booking)
            db.session.commit()
            return redirect(url_for('trekker_bookings'))
            
    return redirect(url_for('trekker_bookings'))


if __name__ == "__main__":
    app.run(debug=True)