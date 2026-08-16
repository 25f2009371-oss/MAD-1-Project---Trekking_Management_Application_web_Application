#we will first import SQLALCHEMY from my flask sqlalchemy library
#model files is basically help us to create our table structure for object relation mapping in simple words 
# connecting my database in instance to my code
#it is model 

from flask_sqlalchemy import SQLAlchemy

#creating my db name var who will have SQLALCHEMY named object
db=SQLAlchemy()

#creating class called Users in which will work as table and have name users
class User(db.Model):
    __tablename__="users"
   user_id=db.Column(db.Integer, primary_key=True,unique=True)
    full_name=db.Column(db.String, nullable=False)
    email=db.Column(db.String, nullable=False,unique=True)
    password=db.Column(db.String, nullable=False)
    Phone=db.Column(db.String,unique=True,nullable=False)
    role=db.Column(db.String,nullable=False)
    bookings = db.relationship("Booking", cascade="all,delete" , backref="bookings")






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
    bookings = db.relationship("Booking", cascade="all,delete", backref="bookings")

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
    assigned_staff_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=True)    
    bookings = db.relationship("Booking", cascade="all,delete", backref="trek")

class Booking(db.Model):
    __tablename__ = "bookings"
    booking_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    trek_id = db.Column(db.Integer, db.ForeignKey("treks.trek_id"), nullable=False)
    booking_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False)
