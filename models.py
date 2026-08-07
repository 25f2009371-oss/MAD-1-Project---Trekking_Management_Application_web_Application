from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  
    phone = db.Column(db.String(15), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    bookings = db.relationship("Booking", cascade="all,delete", backref="user")

class Trek(db.Model):
    __tablename__ = "treks"
    trek_id = db.Column(db.Integer, primary_key=True)
    trek_name = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    difficulty = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    total_slots = db.Column(db.Integer, nullable=False)
    available_slots = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    assigned_staff_id = db.Column(db.Integer, nullable=True)  
    bookings = db.relationship("Booking", cascade="all,delete", backref="trek")

class Booking(db.Model):
    __tablename__ = "bookings"
    booking_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    trek_id = db.Column(db.Integer, db.ForeignKey("treks.trek_id"), nullable=False)
    booking_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False)
