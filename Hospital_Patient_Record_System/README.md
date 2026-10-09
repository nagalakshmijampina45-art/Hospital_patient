# Hospital Patient Record System

A Flask-based Hospital Patient Record and Treatment Tracking System.

## Features

- Patient CRUD operations
- Doctor CRUD operations
- Appointment scheduling and management
- JWT-based authentication
- REST API endpoints
- Pandas and NumPy analytics
- CSV upload
- CSV and Excel export
- Jinja2 HTML templates
- SQLite by default
- MySQL support through SQLAlchemy/PyMySQL

## Project Structure

```text
Hospital_Patient_Record_System/
├── app.py
├── config.py
├── models.py
├── seed.py
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
├── database.sql
├── sample_appointments.csv
├── README.md
├── routes/
│   ├── __init__.py
│   ├── auth.py
│   ├── patients.py
│   ├── doctors.py
│   ├── appointments.py
│   ├── api.py
│   └── analytics.py
├── static/
│   └── style.css
└── templates/
    ├── base.html
    ├── home.html
    ├── login.html
    ├── patients.html
    ├── patient_form.html
    ├── patient_detail.html
    ├── doctors.html
    ├── doctor_form.html
    ├── appointments.html
    ├── appointment_form.html
    ├── appointment_detail.html
    └── analytics.html
```

## Installation

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Install packages:

```bash
pip install -r requirements.txt
```

## Initialize Database

```bash
python seed.py
```

Default login:

```text
Username: admin
Password: admin123
```

## Run

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

## Main Pages

```text
/login
/patients
/patients/new
/doctors
/doctors/new
/appointments
/appointments/new
/analytics
```

## API

Login:

```text
POST /auth/login
```

Patients:

```text
GET    /api/patients
POST   /api/patients
GET    /api/patients/<id>
PUT    /api/patients/<id>
PATCH  /api/patients/<id>
DELETE /api/patients/<id>
```

Doctors:

```text
GET    /api/doctors
POST   /api/doctors
GET    /api/doctors/<id>
PUT    /api/doctors/<id>
PATCH  /api/doctors/<id>
DELETE /api/doctors/<id>
```

Appointments:

```text
GET    /api/appointments
POST   /api/appointments
GET    /api/appointments/<id>
PUT    /api/appointments/<id>
PATCH  /api/appointments/<id>
DELETE /api/appointments/<id>
```

Filter appointments by doctor:

```text
GET /api/appointments?doctor_id=2
```

## Analytics

```text
GET /analytics
GET /analytics/export/csv
GET /analytics/export/excel
```

## MySQL

Create the database using `database.sql`, then update `.env`:

```text
DATABASE_URL=mysql+pymysql://root:password@localhost/hospital_db
```

Then run:

```bash
python seed.py
python app.py
```
