from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False)


class Trek(db.Model):
    trek_id = db.Column(db.Integer, primary_key=True)
    trek_name = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    difficulty = db.Column(db.String, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    total_slots = db.Column(db.Integer, nullable=False)
    available_slots = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    assigned_staff_id = db.Column(db.Integer, nullable=False)


class Booking(db.Model):
    booking_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    trek_id = db.Column(db.Integer, nullable=False)
    booking_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String, nullable=False)