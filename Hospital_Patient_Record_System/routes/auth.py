from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_jwt_extended import create_access_token
from models import db, User

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    username = request.form.get("username")
    password = request.form.get("password")

    user = User.query.filter_by(username=username).first()

    if not user or not user.check_password(password):
        return render_template("login.html", error="Invalid username or password")

    token = create_access_token(
        identity=str(user.id),
        additional_claims={"role": user.role}
    )

    return render_template("home.html", token=token, user=user)

@auth_bp.route("/auth/login", methods=["POST"])
def api_login():
    data = request.get_json() or {}
    user = User.query.filter_by(username=data.get("username")).first()

    if not user or not user.check_password(data.get("password", "")):
        return jsonify({"error": "Invalid username or password"}), 401

    token = create_access_token(
        identity=str(user.id),
        additional_claims={"role": user.role}
    )

    return jsonify({
        "access_token": token,
        "user": {
            "id": user.id,
            "username": user.username,
            "role": user.role
        }
    })
