import os
from flask import Blueprint, render_template, request, session, redirect, url_for, send_from_directory, flash
from models import User
from extensions import db

profile_bp = Blueprint("profile", __name__)

# Upload/config (only for resumes now)
ROOT = os.getcwd()
UPLOAD_DIR = os.path.join(ROOT, "static", "uploads")
RESUMES_DIR = os.path.join(UPLOAD_DIR, "resumes")

ALLOWED_RESUME = {"pdf", "doc", "docx"}

os.makedirs(RESUMES_DIR, exist_ok=True)


# ---------- Profile Page ----------
@profile_bp.route("/profile", methods=["GET", "POST"])
def profile():
    if "user" not in session:
        return redirect(url_for("auth.login"))

    username = session["user"]
    user = User.query.filter_by(username=username).first()

    if not user:
        flash("User not found", "error")
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        # Example: allow updating only email & password
        new_email = request.form.get("email")
        new_password = request.form.get("password")

        if new_email:
            user.email = new_email
        if new_password:
            user.set_password(new_password)

        db.session.commit()
        flash("Profile updated successfully ✅", "success")
        return redirect(url_for("profile.profile"))

    # Always provide default images if user has none
    user.profile_pic = user.profile_pic or "/static/images/default-profile.png"
    user.cover_pic = user.cover_pic or "/static/images/default-cover.jpg"

    return render_template("profile.html", user=user)


# ---------- Resume Download ----------
@profile_bp.route("/profile/download_resume/<username>")
def download_resume(username):
    if "user" not in session:
        return redirect(url_for("auth.login"))

    user = User.query.filter_by(username=username).first()
    if not user or not user.resume:
        flash("No resume uploaded.", "warning")
        return redirect(url_for("profile.profile"))

    filename = os.path.basename(user.resume)
    return send_from_directory(RESUMES_DIR, filename, as_attachment=True)
