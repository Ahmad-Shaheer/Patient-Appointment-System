from flask import Flask, render_template, flash, request
from models import Doctor, Patient, Appointment, Availability
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)


app.config['SECRET_KEY'] = 'healthcare'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///healthcare.db'

db = SQLAlchemy(app)

@app.route('/', methods = ['GET', 'POST'])
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

# @app.route('/dashboard/<int:patient_id>')
# def dashboard(patient_id):
#     patient = db.execute('SELECT * FROM patient WHERE patient_id = ?', (patient_id,)).fetchone()
#     appointments = db.execute('SELECT * FROM appointment WHERE patient_id = ?', (patient_id,)).fetchall()
#     doctors = db.execute('SELECT * FROM doctor').fetchall()
#     return render_template('dashboard.html', patient=patient, appointments=appointments, doctors=doctors)

# from flask import Flask, render_template, request, redirect, url_for
# from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'healthcare'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///healthcare.db'
# db = SQLAlchemy(app)

# # Import models here if not in the same file
# from models import Patient, Appointment

# @app.route('/dashboard')
# def dashboard():
#     patient_id = 1  # Replace with dynamic patient_id from session or query parameter
#     patient = Patient.query.get(patient_id)
#     if patient is None:
#         return "Patient not found", 404

#     appointments = Appointment.query.filter_by(patient_id=patient_id).all()

#     return render_template('dashboard.html', patient=patient, appointments=appointments)

# if __name__ == '__main__':
#     app.run(debug=True)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)