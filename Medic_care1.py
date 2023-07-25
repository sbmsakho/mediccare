from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this to a strong secret key

class Patient:
    def __init__(self, patient_id, first_name, last_name, date_of_birth, gender):
        self.patient_id = patient_id
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.medical_record = {}

patients = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_patient', methods=['POST'])
def add_patient():
    patient_id = request.form['patient_id']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    date_of_birth = request.form['date_of_birth']
    gender = request.form['gender']
    new_patient = Patient(patient_id, first_name, last_name, date_of_birth, gender)
    patients.append(new_patient)
    return redirect('/list_patients')

@app.route('/list_patients')
def list_patients():
    return render_template('list_patients.html', patients=patients)

@app.route('/update_medical_record/<string:patient_id>', methods=['GET', 'POST'])
def update_medical_record(patient_id):
    doctor_username = session.get('doctor_username')

    if doctor_username is None:
        return redirect('/doctor_login')

    patient = None
    for p in patients:
        if p.patient_id == patient_id:
            patient = p
            break

    if patient is None:
        return render_template('patient_not_found.html', patient_id=patient_id)

    if request.method == 'POST':
        diagnosis = request.form['diagnosis']
        prescription = request.form['prescription']

        patient.medical_record['diagnosis'] = diagnosis
        patient.medical_record['prescription'] = prescription

        # Add a note indicating the modification by the doctor
        modification_note = f"Modified by Dr. {doctor_username}"
        patient.medical_record['modification_note'] = modification_note

        return redirect('/list_patients')

    return render_template('update_medical_record.html', patient=patient)

# Doctor login route
@app.route('/doctor_login', methods=['GET', 'POST'])
def doctor_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Add your logic here to authenticate the doctor's credentials
        # For simplicity, let's assume the doctor's username is 'doctor' and password is 'password'

        if username == 'doctor' and password == 'password':
            session['doctor_username'] = username
            return redirect('/list_patients')

    return render_template('doctor_login.html')

@app.route('/view_medical_record/<string:patient_id>')
def view_medical_record(patient_id):
    patient = None
    for p in patients:
        if p.patient_id == patient_id:
            patient = p
            break

    return render_template('view_medical_record.html', patient=patient)

@app.route('/delete_patient/<string:patient_id>', methods=['POST'])
def delete_patient(patient_id):
    for p in patients:
        if p.patient_id == patient_id:
            patients.remove(p)
            break
    
    return redirect('/list_patients')

if __name__ == '__main__':
    app.run(debug=True)


