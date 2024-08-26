from flask import Flask, render_template, flash, request
# from models import Doctor, Patient, Appointment, Availability
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'healthcare'
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


@app.route('/book_appointment', methods = ['GET', 'POST'])
def book_appointment():
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        doctor_id = request.form['doctor_id']
        appointment_date = request.form['appointment_date']
        appointment_status = 'Scheduled'
        try:
            appointment_date = datetime.strptime(appointment_date, '%Y-%m-%d %H:%M')
        except ValueError:
            flash('Invalid date format. Please use YYYY-MM-DD HH:MM.')
        
        new_appointment = Appointment(
            patient_id=patient_id,
            doctor_id=doctor_id,
            appointment_date=appointment_date,
            appointment_status=appointment_status
        )

        # Add and commit the new appointment to the database
        db.session.add(new_appointment)
        db.session.commit()

        flash('Appointment successfully booked!')

    return render_template('book_appointment2.html')


@app.route('/dashboard/<int:patient_id>', methods=['GET'])
def patient_appointment(patient_id):
    patient = Patient.query.get(patient_id)
    if not patient:
        flash('Patient not found.')
        return render_template('dashboard.html')

    appointments = Appointment.query.filter_by(patient_id=patient_id).all()

    return render_template('dashboard.html', patient=patient, appointments=appointments)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)