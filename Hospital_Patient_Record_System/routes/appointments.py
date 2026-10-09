from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Patient, Doctor, Appointment

appointments_bp = Blueprint("appointments", __name__)

@appointments_bp.route("/appointments")
def list_appointments():
    appointments = Appointment.query.order_by(Appointment.date.desc()).all()
    return render_template("appointments.html", appointments=appointments)

@appointments_bp.route("/appointments/new", methods=["GET", "POST"])
def new_appointment():
    patients = Patient.query.all()
    doctors = Doctor.query.all()

    if request.method == "POST":
        appointment = Appointment(
            patient_id=int(request.form["patient_id"]),
            doctor_id=int(request.form["doctor_id"]),
            date=datetime.strptime(request.form["date"], "%Y-%m-%d").date(),
            diagnosis=request.form["diagnosis"],
            status=request.form["status"]
        )
        db.session.add(appointment)
        db.session.commit()
        return redirect(url_for("appointments.list_appointments"))

    return render_template(
        "appointment_form.html",
        appointment=None,
        patients=patients,
        doctors=doctors
    )

@appointments_bp.route("/appointments/<int:id>")
def appointment_detail(id):
    appointment = Appointment.query.get_or_404(id)
    return render_template(
        "appointment_detail.html",
        appointment=appointment
    )

@appointments_bp.route("/appointments/<int:id>/edit", methods=["GET", "POST"])
def edit_appointment(id):
    appointment = Appointment.query.get_or_404(id)
    patients = Patient.query.all()
    doctors = Doctor.query.all()

    if request.method == "POST":
        appointment.patient_id = int(request.form["patient_id"])
        appointment.doctor_id = int(request.form["doctor_id"])
        appointment.date = datetime.strptime(
            request.form["date"], "%Y-%m-%d"
        ).date()
        appointment.diagnosis = request.form["diagnosis"]
        appointment.status = request.form["status"]
        db.session.commit()

        return redirect(url_for(
            "appointments.appointment_detail", id=id
        ))

    return render_template(
        "appointment_form.html",
        appointment=appointment,
        patients=patients,
        doctors=doctors
    )

@appointments_bp.route("/appointments/<int:id>", methods=["PUT", "DELETE"])
def appointment_update_api(id):
    appointment = Appointment.query.get_or_404(id)

    if request.method == "DELETE":
        db.session.delete(appointment)
        db.session.commit()
        return {"message": "Appointment cancelled successfully"}

    data = request.get_json() or {}

    if "patient_id" in data:
        appointment.patient_id = data["patient_id"]
    if "doctor_id" in data:
        appointment.doctor_id = data["doctor_id"]
    if "date" in data:
        appointment.date = datetime.strptime(
            data["date"], "%Y-%m-%d"
        ).date()
    if "diagnosis" in data:
        appointment.diagnosis = data["diagnosis"]
    if "status" in data:
        appointment.status = data["status"]

    db.session.commit()
    return {"message": "Appointment updated successfully"}
