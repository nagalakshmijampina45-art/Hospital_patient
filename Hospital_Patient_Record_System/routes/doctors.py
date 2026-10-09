from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Doctor

doctors_bp = Blueprint("doctors", __name__)

@doctors_bp.route("/doctors")
def list_doctors():
    doctors = Doctor.query.order_by(Doctor.id.desc()).all()
    return render_template("doctors.html", doctors=doctors)

@doctors_bp.route("/doctors/new", methods=["GET", "POST"])
def new_doctor():
    if request.method == "POST":
        doctor = Doctor(
            name=request.form["name"],
            specialization=request.form["specialization"]
        )
        db.session.add(doctor)
        db.session.commit()
        return redirect(url_for("doctors.list_doctors"))

    return render_template("doctor_form.html", doctor=None)

@doctors_bp.route("/doctors/<int:id>/edit", methods=["GET", "POST"])
def edit_doctor(id):
    doctor = Doctor.query.get_or_404(id)

    if request.method == "POST":
        doctor.name = request.form["name"]
        doctor.specialization = request.form["specialization"]
        db.session.commit()
        return redirect(url_for("doctors.list_doctors"))

    return render_template("doctor_form.html", doctor=doctor)

@doctors_bp.route("/doctors/<int:id>", methods=["DELETE"])
def delete_doctor(id):
    doctor = Doctor.query.get_or_404(id)
    db.session.delete(doctor)
    db.session.commit()
    return {"message": "Doctor deleted successfully"}
