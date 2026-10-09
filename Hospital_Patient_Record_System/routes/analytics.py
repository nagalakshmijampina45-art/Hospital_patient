from flask import Blueprint, render_template, request, send_file, flash
from models import Appointment
import pandas as pd
import numpy as np
import os

analytics_bp = Blueprint("analytics", __name__)

@analytics_bp.route("/analytics", methods=["GET", "POST"])
def analytics():
    appointments = Appointment.query.all()

    data = [{
        "id": a.id,
        "date": a.date,
        "doctor": a.doctor.name,
        "diagnosis": a.diagnosis,
        "status": a.status
    } for a in appointments]

    df = pd.DataFrame(data)

    if df.empty:
        stats = {
            "total": 0,
            "common_diagnosis": "No data",
            "recovered_rate": 0,
            "statuses": {},
            "doctor_performance": []
        }
    else:
        common_diagnosis = df["diagnosis"].value_counts().idxmax()
        recovered_rate = round(
            (df["status"].eq("Recovered").mean()) * 100, 2
        )

        doctor_performance = (
            df.groupby("doctor")
            .agg(
                patients_treated=("id", "count"),
                recovery_rate=("status", lambda x:
                    round((x == "Recovered").mean() * 100, 2))
            )
            .reset_index()
            .to_dict("records")
        )

        stats = {
            "total": len(df),
            "common_diagnosis": common_diagnosis,
            "recovered_rate": recovered_rate,
            "statuses": df["status"].value_counts().to_dict(),
            "doctor_performance": doctor_performance
        }

    if request.method == "POST" and "file" in request.files:
        uploaded = request.files["file"]

        if uploaded.filename.endswith(".csv"):
            upload_dir = "uploads"
            os.makedirs(upload_dir, exist_ok=True)
            path = os.path.join(upload_dir, uploaded.filename)
            uploaded.save(path)
            flash("CSV uploaded successfully.")

    return render_template("analytics.html", stats=stats)

@analytics_bp.route("/analytics/export/csv")
def export_csv():
    appointments = Appointment.query.all()

    data = [{
        "id": a.id,
        "patient": a.patient.name,
        "doctor": a.doctor.name,
        "date": a.date,
        "diagnosis": a.diagnosis,
        "status": a.status
    } for a in appointments]

    df = pd.DataFrame(data)
    os.makedirs("reports", exist_ok=True)

    path = "reports/analytics.csv"
    df.to_csv(path, index=False)

    return send_file(path, as_attachment=True)

@analytics_bp.route("/analytics/export/excel")
def export_excel():
    appointments = Appointment.query.all()

    data = [{
        "id": a.id,
        "patient": a.patient.name,
        "doctor": a.doctor.name,
        "date": a.date,
        "diagnosis": a.diagnosis,
        "status": a.status
    } for a in appointments]

    df = pd.DataFrame(data)
    os.makedirs("reports", exist_ok=True)

    path = "reports/analytics.xlsx"
    df.to_excel(path, index=False)

    return send_file(path, as_attachment=True)
