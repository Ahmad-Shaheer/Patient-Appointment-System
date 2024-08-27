from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/doctor-login')
def doctor_login():
    return render_template('doctor-login.html')

@app.route('/patient-login')
def patient_login():
    return render_template('patient-login.html')

@app.route('/dashboard', methods=['GET'])
def patient_dashborad():
    # patient = Patient.query.get(patient_id)
    # if not patient:
    #     flash('Patient not found.')
        return render_template('dashboard.html')
if __name__ == '__main__':
    app.run(debug=True)
