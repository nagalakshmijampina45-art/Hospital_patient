from datetime import date, timedelta
from app import app
from models import db, User, Patient, Doctor, Appointment

with app.app_context():
    db.create_all()

    if not User.query.filter_by(username="admin").first():
        user = User(username="admin", role="admin")
        user.set_password("admin123")
        db.session.add(user)

    if Patient.query.count() == 0:
        patients = [
            Patient(name="Ravi Kumar", age=35, gender="Male", contact="9876543210"),
            Patient(name="Sita Devi", age=29, gender="Female", contact="9876543211"),
            Patient(name="Arjun Rao", age=46, gender="Male", contact="9876543212")
        ]
        db.session.add_all(patients)

    if Doctor.query.count() == 0:
        doctors = [
            Doctor(name="Dr. Priya", specialization="Cardiology"),
            Doctor(name="Dr. Anand", specialization="Neurology"),
            Doctor(name="Dr. Meena", specialization="General Medicine")
        ]
        db.session.add_all(doctors)

    db.session.commit()

    if Appointment.query.count() == 0:
        patients = Patient.query.all()
        doctors = Doctor.query.all()
        appointments = [
            Appointment(
                patient_id=patients[0].id,
                doctor_id=doctors[0].id,
                date=date.today() - timedelta(days=10),
                diagnosis="Heart Disease",
                status="Recovered"
            ),
            Appointment(
                patient_id=patients[1].id,
                doctor_id=doctors[1].id,
                date=date.today() - timedelta(days=5),
                diagnosis="Migraine",
                status="Under Treatment"
            ),
            Appointment(
                patient_id=patients[2].id,
                doctor_id=doctors[2].id,
                date=date.today(),
                diagnosis="Fever",
                status="Critical"
            )
        ]
        db.session.add_all(appointments)

    db.session.commit()
    print("Database seeded successfully.")
    print("Admin username: admin")
    print("Admin password: admin123")
