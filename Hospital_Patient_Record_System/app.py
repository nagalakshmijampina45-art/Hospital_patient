from flask import Flask, render_template
from flask_jwt_extended import JWTManager
from config import Config
from models import db

from routes.auth import auth_bp
from routes.patients import patients_bp
from routes.doctors import doctors_bp
from routes.appointments import appointments_bp
from routes.api import api_bp
from routes.analytics import analytics_bp


app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)

jwt = JWTManager(app)


app.register_blueprint(auth_bp)
app.register_blueprint(patients_bp)
app.register_blueprint(doctors_bp)
app.register_blueprint(appointments_bp)
app.register_blueprint(api_bp)
app.register_blueprint(analytics_bp)


@app.route("/")
def home():
    return render_template("home.html")


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)