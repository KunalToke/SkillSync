from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import re
from extensions import db
from models.user import User  # import the correct model

auth_bp = Blueprint("auth", __name__)

# ----------------- JOB SEEKER REGISTRATION -----------------
@auth_bp.route("/register-jobseeker", methods=["GET", "POST"])
def register_jobseeker():
    if request.method == "POST":
        email = (request.form.get("email") or "").strip()
        username = (request.form.get("username") or "").strip()
        password = (request.form.get("password") or "").strip()

        if not email or not username or not password:
            flash("Please fill out all required fields.", "error")
            return redirect(url_for("auth.register_jobseeker"))

        # Check if user already exists
        existing_user = User.query.filter(
            (User.email == email) | (User.username == username)
        ).first()
        if existing_user:
            flash("Email or Username already registered.", "error")
            return redirect(url_for("auth.register_jobseeker"))

        # Password validation
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$', password):
            flash("Password must be 8+ chars with uppercase, lowercase, number, and special char.", "error")
            return redirect(url_for("auth.register_jobseeker"))

        # Create new Job Seeker user (model uses 'role' field)
        new_user = User(
            email=email,
            username=username,
            role="job_seeker"
        )
        new_user.set_password(password)  # hash password
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Please login.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register_jobseeker.html")


# ----------------- TALENT SEEKER REGISTRATION -----------------
@auth_bp.route("/register-talentseeker", methods=["GET", "POST"])
def register_talentseeker():
    if request.method == "POST":
        email = (request.form.get("email") or "").strip()
        username = (request.form.get("username") or "").strip()
        password = (request.form.get("password") or "").strip()
        company_name = (request.form.get("company_name") or "").strip()

        if not email or not username or not password or not company_name:
            flash("Please fill out all required fields.", "error")
            return redirect(url_for("auth.register_talentseeker"))

        existing_user = User.query.filter(
            (User.email == email) | (User.username == username)
        ).first()
        if existing_user:
            flash("Email or Username already registered.", "error")
            return redirect(url_for("auth.register_talentseeker"))

        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$', password):
            flash("Password must be 8+ chars with uppercase, lowercase, number, and special char.", "error")
            return redirect(url_for("auth.register_talentseeker"))

        new_user = User(
            email=email,
            username=username,
            role="talent_seeker",
            company_name=company_name
        )
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Please login.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register_talentseeker.html")


# ----------------- LOGIN -----------------
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # read and clean inputs
        identifier = (request.form.get("username_or_email") or "").strip()
        password = (request.form.get("password") or "").strip()

        if not identifier or not password:
            flash("Please enter both username/email and password.", "error")
            return redirect(url_for("auth.login"))

        # find by email OR username
        user = User.query.filter(
            (User.email == identifier) | (User.username == identifier)
        ).first()

        # generic error message so we don't leak which part failed
        if not user or not user.check_password(password):
            flash("Invalid username/email or password.", "danger")
            return redirect(url_for("auth.login"))

        # login success — save session
        session["user"] = user.username
        # support either attribute name on the model: user_type (preferred) or role (older)
        role = getattr(user, "user_type", None) or getattr(user, "role", None)
        session["role"] = role

        flash(f"Welcome back, {user.username}!", "success")

        # redirect based on role
        if role == "job_seeker":
            return redirect(url_for("job_seekers.dashboard"))
        if role == "talent_seeker":
            return redirect(url_for("talent_seekers.dashboard"))

        # fallback
        return redirect(url_for("home"))

    return render_template("login.html")

# ----------------- LOGOUT -----------------
@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("home"))
