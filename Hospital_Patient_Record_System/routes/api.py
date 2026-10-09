from flask import Blueprint, request, jsonify
from models import db, Patient, Doctor, Appointment
from flask_jwt_extended import jwt_required

api_bp = Blueprint("api", __name__, url_prefix="/api")

def patient_dict(p):
    return {
        "id": p.id,
        "name": p.name,
        "age": p.age,
        "gender": p.gender,
        "contact": p.contact
    }

def doctor_dict(d):
    return {
        "id": d.id,
        "name": d.name,
        "specialization": d.specialization
    }

def appointment_dict(a):
    return {
        "id": a.id,
        "patient_id": a.patient_id,
        "doctor_id": a.doctor_id,
        "date": a.date.isoformat(),
        "diagnosis": a.diagnosis,
        "status": a.status
    }

@api_bp.route("/patients", methods=["GET", "POST"])
@jwt_required(optional=True)
def patients_api():
    if request.method == "GET":
        return jsonify([patient_dict(p) for p in Patient.query.all()])

    data = request.get_json() or {}
    required = ["name", "age", "gender", "contact"]

    if any(field not in data for field in required):
        return jsonify({"error": "All patient fields are required"}), 400

    patient = Patient(
        name=data["name"],
        age=data["age"],
        gender=data["gender"],
        contact=data["contact"]
    )
    db.session.add(patient)
    db.session.commit()

    return jsonify(patient_dict(patient)), 201

@api_bp.route("/patients/<int:id>", methods=["GET", "PUT", "PATCH", "DELETE"])
@jwt_required(optional=True)
def patient_api(id):
    patient = Patient.query.get_or_404(id)

    if request.method == "GET":
        return jsonify(patient_dict(patient))

    if request.method == "DELETE":
        db.session.delete(patient)
        db.session.commit()
        return jsonify({"message": "Patient deleted"})

    data = request.get_json() or {}

    for field in ["name", "age", "gender", "contact"]:
        if field in data:
            setattr(patient, field, data[field])

    db.session.commit()
    return jsonify(patient_dict(patient))

@api_bp.route("/doctors", methods=["GET", "POST"])
@jwt_required(optional=True)
def doctors_api():
    if request.method == "GET":
        return jsonify([doctor_dict(d) for d in Doctor.query.all()])

    data = request.get_json() or {}
    if "name" not in data or "specialization" not in data:
        return jsonify({"error": "name and specialization are required"}), 400

    doctor = Doctor(
        name=data["name"],
        specialization=data["specialization"]
    )
    db.session.add(doctor)
    db.session.commit()

    return jsonify(doctor_dict(doctor)), 201

@api_bp.route("/doctors/<int:id>", methods=["GET", "PUT", "PATCH", "DELETE"])
@jwt_required(optional=True)
def doctor_api(id):
    doctor = Doctor.query.get_or_404(id)

    if request.method == "GET":
        return jsonify(doctor_dict(doctor))

    if request.method == "DELETE":
        db.session.delete(doctor)
        db.session.commit()
        return jsonify({"message": "Doctor deleted"})

    data = request.get_json() or {}
    doctor.name = data.get("name", doctor.name)
    doctor.specialization = data.get(
        "specialization", doctor.specialization
    )
    db.session.commit()

    return jsonify(doctor_dict(doctor))

@api_bp.route("/appointments", methods=["GET", "POST"])
@jwt_required(optional=True)
def appointments_api():
    doctor_id = request.args.get("doctor_id")

    query = Appointment.query

    if doctor_id:
        query = query.filter_by(doctor_id=int(doctor_id))

    if request.method == "GET":
        return jsonify([appointment_dict(a) for a in query.all()])

    data = request.get_json() or {}
    required = ["patient_id", "doctor_id", "date", "diagnosis", "status"]

    if any(field not in data for field in required):
        return jsonify({"error": "All appointment fields are required"}), 400

    from datetime import datetime

    appointment = Appointment(
        patient_id=data["patient_id"],
        doctor_id=data["doctor_id"],
        date=datetime.strptime(data["date"], "%Y-%m-%d").date(),
        diagnosis=data["diagnosis"],
        status=data["status"]
    )

    db.session.add(appointment)
    db.session.commit()

    return jsonify(appointment_dict(appointment)), 201

@api_bp.route("/appointments/<int:id>", methods=["GET", "PUT", "PATCH", "DELETE"])
@jwt_required(optional=True)
def appointment_api(id):
    appointment = Appointment.query.get_or_404(id)

    if request.method == "GET":
        return jsonify(appointment_dict(appointment))

    if request.method == "DELETE":
        db.session.delete(appointment)
        db.session.commit()
        return jsonify({"message": "Appointment deleted"})

    data = request.get_json() or {}

    if "patient_id" in data:
        appointment.patient_id = data["patient_id"]
    if "doctor_id" in data:
        appointment.doctor_id = data["doctor_id"]
    if "date" in data:
        from datetime import datetime
        appointment.date = datetime.strptime(
            data["date"], "%Y-%m-%d"
        ).date()
    if "diagnosis" in data:
        appointment.diagnosis = data["diagnosis"]
    if "status" in data:
        appointment.status = data["status"]

    db.session.commit()
    return jsonify(appointment_dict(appointment))
