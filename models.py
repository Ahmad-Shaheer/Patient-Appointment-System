from flask import Flask
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET KEY'] = 'healthcare'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///healthcare.db'


db = SQLAlchemy(app)

class Patient(db.Model):
    patient_id = db.Column(db.Integer, primary_key = True, nullable=False)
    first_name  = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.DateTime, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    appointments = db.relationship('Appointment', backref = 'patient', lazy = True)
    
class Doctor(db.Model):
    doctor_id = db.Column(db.Integer, primary_key = True)
    first_name  = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    appointments = db.relationship('Appointment', backref = 'doctor', lazy = True)
    availability = db.relationship('Availability', backref = 'doctor', lazy = True)

class Appointment(db.Model):
    appointment_id = db.Column(db.Integer, primary_key = True, nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey("patient.patient_id"), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctor.doctor_id"), nullable=False)
    appointment_date = db.Column(db.DateTime, nullable=False)
    appointment_status = db.Column(db.String(80), nullable=False)

class Availability(db.Model):
    availability_id = db.Column(db.Integer, primary_key = True, nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.doctor_id'), nullable=False)
    available_start_time = db.Column(db.DateTime, nullable=False)
    available_end_time = db.Column(db.DateTime, nullable=False)
    
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
    
    
        