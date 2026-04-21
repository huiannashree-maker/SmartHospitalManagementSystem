Smart Hospital Management System (MedConnect)
A comprehensive healthcare administration platform built with Flask and MongoDB. This system streamlines the patient-to-doctor pipeline through an automated triage logic, centralized administrative oversight, and dedicated professional dashboards.


🚀 Key Features
1. Role-Based Access Control (RBAC)
Admin Dashboard: Full control over the medical staff directory. Admins approve or reject patient requests before they reach the doctor's queue.

Doctor Dashboard: A live "Live Portal" for practitioners to manage their active patient queue, toggle their availability status, and update their professional profiles.
Patient Dashboard: An intuitive interface for symptom self-assessment, appointment booking, and tracking personal medical history.

3. Rule-Based Symptom Analyzer
Automated triage logic that maps user-described symptoms to specific medical conditions and specialties.
Suggests the most relevant doctor based on specialization and availability.


5. Digital Record Management
Eliminates paper-based tracking by storing all patient requests, staff details, and booking history in a NoSQL (MongoDB) environment.
Format-consistent history tracking (DD-MM-YYYY).


🛠️ Tech Stack
Backend: Python 3.x, Flask
Database: MongoDB (NoSQL)
Frontend: HTML5, CSS3, Bootstrap 5, Jinja2
Icons & UI: Bootstrap Icons, Animate.css


📂 Project Structure
├── app.py              # Main application logic & routes
├── engine.py           # Symptom analysis & logic engine
├── models.py           # MongoDB connection & configuration
├── static/
│   ├── css/            # Custom styles
│   └── profile_pics/   # Uploaded doctor headshots
└── templates/          # Jinja2 HTML templates
    ├── admin.html
    ├── doctor_dashboard.html
    ├── patient_dashboard.html
    └── layout.html
  
   
   ⚙️ Installation & Setup
   1.Clone the repository:
   git clone https://github.com/huiannashree-maker/SmartHospitalManagementSystem.git
cd SmartHospitalManagementSystem

2.Create a Virtual Environment:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3.Install Dependencies:
pip install flask pymongo werkzeug

4.Database Configuration:
Ensure MongoDB Compass is running.
Update the connection string in models.py if necessary.

5.Run the Application:
python app.py

 
 
 System Workflow
Patient enters symptoms \rightarrow Analyzer suggests condition/specialty.
Patient submits a request \rightarrow Data moves to Admin "Pending" list.
Admin reviews and approves \rightarrow Request moves to specific Doctor's queue.
Doctor completes session \rightarrow Request marked "Completed" in Patient history.


Conclusion
This project demonstrates a modernized approach to clinical operations, focusing on user experience and administrative transparency. It serves as a scalable foundation for future AI integration and advanced Electronic Health Records (EHR

