from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Patient

patients_bp = Blueprint("patients", __name__)

@patients_bp.route("/patients")
def list_patients():
    patients = Patient.query.order_by(Patient.id.desc()).all()
    return render_template("patients.html", patients=patients)

@patients_bp.route("/patients/new", methods=["GET", "POST"])
def new_patient():
    if request.method == "POST":
        patient = Patient(
            name=request.form["name"],
            age=int(request.form["age"]),
            gender=request.form["gender"],
            contact=request.form["contact"]
        )
        db.session.add(patient)
        db.session.commit()
        return redirect(url_for("patients.list_patients"))

    return render_template("patient_form.html", patient=None)

@patients_bp.route("/patients/<int:id>")
def patient_detail(id):
    patient = Patient.query.get_or_404(id)
    return render_template("patient_detail.html", patient=patient)

@patients_bp.route("/patients/<int:id>/edit", methods=["GET", "POST"])
def edit_patient(id):
    patient = Patient.query.get_or_404(id)

    if request.method == "POST":
        patient.name = request.form["name"]
        patient.age = int(request.form["age"])
        patient.gender = request.form["gender"]
        patient.contact = request.form["contact"]
        db.session.commit()
        return redirect(url_for("patients.patient_detail", id=id))

    return render_template("patient_form.html", patient=patient)

@patients_bp.route("/patients/<int:id>", methods=["PUT", "PATCH", "DELETE"])
def patient_update_api(id):
    patient = Patient.query.get_or_404(id)

    if request.method == "DELETE":
        db.session.delete(patient)
        db.session.commit()
        return {"message": "Patient deleted successfully"}

    data = request.get_json() or {}

    if request.method == "PUT":
        patient.name = data.get("name", patient.name)
        patient.age = data.get("age", patient.age)
        patient.gender = data.get("gender", patient.gender)
        patient.contact = data.get("contact", patient.contact)
    else:
        if "name" in data:
            patient.name = data["name"]
        if "age" in data:
            patient.age = data["age"]
        if "gender" in data:
            patient.gender = data["gender"]
        if "contact" in data:
            patient.contact = data["contact"]

    db.session.commit()
    return {"message": "Patient updated successfully"}
