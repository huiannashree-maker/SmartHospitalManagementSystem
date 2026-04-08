from flask import Flask, render_template, request, redirect, url_for, session, flash
from engine import analyze_symptoms
from models import get_mongo_connection
from bson.objectid import ObjectId
from datetime import datetime
import os
from werkzeug.utils import secure_filename

# Corrected __name__ with double underscores
app = Flask(__name__)
app.secret_key = "medconnect_secure_key_2026"
db = get_mongo_connection()

# Upload Settings
UPLOAD_FOLDER = 'static/profile_pics'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# --- AUTHENTICATION ---

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for(f"{session['role']}_dashboard"))
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        name = request.form.get('name', 'New User')
        age = request.form.get('age', 'N/A')

        if db.users.find_one({"email": email}):
            flash("User already exists!", "warning")
            return redirect(url_for('signup'))

        db.users.insert_one({
            "email": email,
            "password": password,
            "role": role,
            "name": name,
            "age": age
        })

        if role == 'doctor':
            db.doctors.insert_one({
                "email": email,
                "name": name,
                "specialization": "General Physician",
                "available": True
            })

        flash("Registration successful!", "success")
        return redirect(url_for('index'))
    return render_template('signup.html')


@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    role = request.form.get('role')
    user = db.users.find_one({"email": email, "password": password, "role": role})

    if user:
        session.update({'user_id': str(user['_id']), 'role': role, 'email': email})
        return redirect(url_for(f"{role}_dashboard"))

    flash("Invalid credentials.", "danger")
    return redirect(url_for('index'))


# --- ADMIN ROUTES ---

@app.route('/admin_dashboard')
def admin_dashboard():
    if session.get('role') != 'admin': return redirect(url_for('index'))

    doctors = list(db.doctors.find())
    pending_requests = list(db.patient_requests.find({"status": "pending"}))

    for req in pending_requests:
        patient = db.users.find_one({"_id": ObjectId(req['patient_id'])})
        if patient:
            req['patient_name'] = patient.get('name', 'Unknown')
            req['patient_age'] = patient.get('age', 'N/A')
            req['condition'] = req.get('reason') or req.get('condition') or "General"

    return render_template('admin.html', doctors=doctors, requests=pending_requests)


@app.route('/admin/add_doctor', methods=['POST'])
def add_doctor():
    if session.get('role') != 'admin': return redirect(url_for('index'))
    db.doctors.insert_one({
        "name": request.form.get('name'),
        "email": request.form.get('email'),
        "specialization": request.form.get('specialty'),
        "age": request.form.get('age'),
        "contact_number": request.form.get('contact'),
        "available": True
    })
    flash("New staff registered!", "success")
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/handle_request/<id>/<action>')
def handle_request(id, action):
    if session.get('role') != 'admin': return redirect(url_for('index'))
    status = "approved" if action == "accept" else "rejected"
    db.patient_requests.update_one({"_id": ObjectId(id)}, {"$set": {"status": status}})
    flash(f"Request {status}!", "info")
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/delete_doctor/<id>')
def delete_doctor(id):
    if session.get('role') != 'admin': return redirect(url_for('index'))
    db.doctors.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('admin_dashboard'))


# --- DOCTOR ROUTES ---

@app.route('/doctor_dashboard')
def doctor_dashboard():
    if session.get('role') != 'doctor': return redirect(url_for('index'))

    doc = db.doctors.find_one({"email": session['email']})

    # Logic to fetch patients assigned to this doctor's specialty
    patients = list(db.patient_requests.find({
        "specialty": doc.get('specialization'),
        "status": "approved"
    }))

    for p in patients:
        p['condition'] = p.get('reason') or p.get('condition') or "Consultation"

    return render_template('doctor_dashboard.html', profile=doc, patients=patients)


@app.route('/doctor/toggle_status')
def toggle_status():
    if session.get('role') != 'doctor': return redirect(url_for('index'))
    doc = db.doctors.find_one({"email": session['email']})
    new_status = not doc.get('available', True)
    db.doctors.update_one({"email": session['email']}, {"$set": {"available": new_status}})
    return redirect(url_for('doctor_dashboard'))


@app.route('/doctor/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if session.get('role') != 'doctor': return redirect(url_for('index'))

    if request.method == 'POST':
        new_name = request.form.get('name')
        new_age = request.form.get('age')

        # Update both collections to keep data consistent
        db.doctors.update_one({"email": session['email']}, {"$set": {
            "name": new_name,
            "specialization": request.form.get('specialty'),
            "contact_number": request.form.get('contact'),
            "age": new_age
        }})
        db.users.update_one({"email": session['email']}, {"$set": {
            "name": new_name,
            "age": new_age
        }})

        flash("Profile Updated Successfully!", "success")
        return redirect(url_for('doctor_dashboard'))

    profile = db.doctors.find_one({"email": session['email']})
    return render_template('edit_profile.html', profile=profile)


@app.route('/doctor/upload_pic', methods=['POST'])
def upload_pic():
    if session.get('role') != 'doctor': return redirect(url_for('index'))
    file = request.files.get('profile_pic')
    if file and file.filename:
        filename = secure_filename(f"{session['user_id']}_{file.filename}")
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        db.doctors.update_one({"email": session['email']}, {"$set": {"pic": filename}})
    return redirect(url_for('doctor_dashboard'))


# --- PATIENT DASHBOARD & ACTIONS ---

@app.route('/patient_dashboard', methods=['GET', 'POST'])
def patient_dashboard():
    if session.get('role') != 'patient': return redirect(url_for('index'))

    user_data = db.users.find_one({"_id": ObjectId(session['user_id'])})
    history = list(db.patient_requests.find({"patient_id": session['user_id']}).sort("_id", -1))

    for item in history:
        item['condition'] = item.get('reason') or item.get('condition') or "Checkup"

    result = None
    if request.method == 'POST':
        symptoms = request.form.get('symptoms')
        analysis = analyze_symptoms(symptoms)

        req_specialty = analysis.get('specialty', 'General Physician')
        doc = db.doctors.find_one({"specialization": req_specialty}) or \
              db.doctors.find_one({"specialization": "General Physician"})

        result = {
            "condition": analysis.get('condition', 'Under Review'),
            "doctor_name": doc.get('name', 'Staff on Duty') if doc else 'Staff on Duty',
            "doctor_specialty": doc.get('specialization', 'General'),
            "doctor_contact": doc.get('contact_number') or doc.get('contact_details') or 'N/A'
        }
        session['last_analysis'] = result

    return render_template('patient_dashboard.html', user=user_data, result=result, history=history)


@app.route('/book_appointment', methods=['POST'])
def book_appointment():
    if 'last_analysis' not in session:
        flash("Analyze symptoms first!", "warning")
        return redirect(url_for('patient_dashboard'))

    analysis = session['last_analysis']
    db.patient_requests.insert_one({
        "patient_id": session['user_id'],
        "reason": analysis['condition'],
        "doctor": analysis['doctor_name'],
        "specialty": analysis['doctor_specialty'],
        "status": "pending",
        "date": datetime.now().strftime("%d-%m-%Y")
    })
    session.pop('last_analysis', None)
    flash("Appointment Booked Successfully!", "success")
    return redirect(url_for('patient_dashboard'))


@app.route('/reset_analysis')
def reset_analysis():
    session.pop('last_analysis', None)
    return redirect(url_for('patient_dashboard'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


# Corrected __name__ and __main__ with double underscores
if __name__ == '__main__':
    app.run(debug=True)