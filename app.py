from flask import Flask, render_template, session, redirect, url_for
from extensions import db   # Database instance

# ---------- Import Blueprints ----------
from routes.auth import auth_bp
from routes.profile import profile_bp
from routes.resume import resume_bp
from routes.career import career_bp
from routes.matching import matching_bp
from routes.skills import skills_bp
from routes.interview import interview_bp
from routes.alerts import alerts_bp
from routes.career_path import career_path_bp
from routes.talent_seekers import talent_seekers_bp
from routes.messaging import messaging_bp
from routes.reviews import reviews_bp
from routes.job_seekers import job_seekers_bp

# ---------- Import Jobs Data ----------
from models.jobs import jobs_by_company

# ---------- App Initialization ----------
app = Flask(__name__)
import os
app.secret_key = os.environ.get("SECRET_KEY", "fallback_secret")


# ---------- Database Configuration ----------
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///career_platform.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# ---------- Register Blueprints ----------
app.register_blueprint(auth_bp, url_prefix="/auth")         
app.register_blueprint(profile_bp)
app.register_blueprint(resume_bp)
app.register_blueprint(career_bp)
app.register_blueprint(matching_bp)
app.register_blueprint(skills_bp)
app.register_blueprint(interview_bp)
app.register_blueprint(alerts_bp)
app.register_blueprint(career_path_bp)
app.register_blueprint(talent_seekers_bp, url_prefix="/talent-seekers")  
app.register_blueprint(job_seekers_bp, url_prefix="/job-seekers")        
app.register_blueprint(messaging_bp)
app.register_blueprint(reviews_bp)

# ---------- Main Routes ----------
@app.route("/")
def home():
    """Main homepage: user selects Job Seeker or Talent Seeker"""
    return render_template("home.html")

@app.route("/logout")
def logout():
    """Logout user and redirect to homepage"""
    session.pop("user", None)
    session.pop("role", None)
    return redirect(url_for("home"))

@app.route("/job_alerts")
def job_alerts():
    """Optional: Job Alerts Page"""
    return render_template("job_alerts.html", jobs=jobs_by_company)

@app.route("/dashboard")
def dashboard():
    """Redirect users to the correct dashboard based on role"""
    if "user" not in session:
        return redirect(url_for("auth.login"))

    role = session.get("role")
    if role == "job_seeker":
        # Redirect to Job Seeker dashboard
        return redirect(url_for("job_seekers.dashboard"))
    elif role == "talent_seeker":
        # Redirect to Talent Seeker dashboard
        return redirect(url_for("talent_seekers.dashboard"))

    # Fallback: generic dashboard if role missing
    return render_template("dashboard.html", username=session.get("user"))

# ---------- Run App ----------
if __name__ == "__main__":
    app.run(debug=True)
