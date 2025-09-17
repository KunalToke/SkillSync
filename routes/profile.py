import os
import json
from datetime import datetime
from flask import Blueprint, render_template, request, session, redirect, url_for, send_from_directory, flash, jsonify
from werkzeug.utils import secure_filename

# Import DB model functions
try:
    from models.user import (
        get_user_by_username,
        update_profile,
        update_profile_pic,
        update_cover_pic
    )
except Exception:
    get_user_by_username = None
    update_profile = None
    update_profile_pic = None
    update_cover_pic = None

# Import roadmap progress helper
try:
    from models.roadmap import get_user_roadmap_progress
except Exception:
    def get_user_roadmap_progress(username):
        return 0

profile_bp = Blueprint("profile", __name__)

# Upload/config
ROOT = os.getcwd()
UPLOAD_DIR = os.path.join(ROOT, "static", "uploads")
PROFILE_PICS = os.path.join(UPLOAD_DIR, "profile_pics")
COVER_PICS = os.path.join(UPLOAD_DIR, "cover_pics")
RESUMES_DIR = os.path.join(UPLOAD_DIR, "resumes")
DATA_DIR = os.path.join(ROOT, "data", "users")

ALLOWED_RESUME = {"pdf", "doc", "docx"}
ALLOWED_IMG = {"png", "jpg", "jpeg", "gif"}

os.makedirs(PROFILE_PICS, exist_ok=True)
os.makedirs(COVER_PICS, exist_ok=True)
os.makedirs(RESUMES_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)


def allowed_file(filename, allowed_set):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_set


def user_json_path(username):
    return os.path.join(DATA_DIR, f"{username}.json")


def load_user_from_json(username):
    path = user_json_path(username)
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None
    return None


def save_user_to_json(username, data):
    path = user_json_path(username)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def ensure_default_user(username):
    user = None
    if get_user_by_username:
        try:
            user = get_user_by_username(username)
        except Exception:
            user = None

    if not user:
        user = load_user_from_json(username)

    if not user:
        user = {
            "username": username,
            "name": username,
            "headline": "",
            "location": "",
            "relocation": "No",
            "contact_email": "",
            "contact_phone": "",
            "profile_pic": "/static/images/default-profile.png",
            "cover_pic": "/static/images/default-cover.jpg",
            "about": "",
            "skills": [],
            "education": [],
            "experience": [],
            "portfolio": {"github": "", "linkedin": "", "behance": ""},
            "resume": "",
            "roadmap_progress": 0,
            "assessments": [],
            "certificates": [],
            "job_preferences": {"role": "", "salary": "", "work_type": ""},
            "saved_jobs": [],
            "applied_jobs": [],
            "endorsements": [],
            "timeline": [],
            "achievements": [],
            "visibility": "public",
            "resume_sharing": True,
            "last_updated": None,
        }
        save_user_to_json(username, user)

    # Ensure keys exist
    user.setdefault("portfolio", {"github": "", "linkedin": "", "behance": ""})
    user.setdefault("skills", [])
    user.setdefault("education", [])
    user.setdefault("experience", [])
    user.setdefault("saved_jobs", [])
    user.setdefault("applied_jobs", [])
    user.setdefault("job_preferences", {"role": "", "salary": "", "work_type": ""})

    return user


# ---------- Profile Pic Upload ----------
@profile_bp.route("/profile/upload_pic", methods=["POST"])
def upload_pic():
    if "user" not in session:
        return jsonify({"success": False, "message": "Login required"}), 401

    username = session["user"]
    file = request.files.get("file")
    if file and allowed_file(file.filename, ALLOWED_IMG):
        ext = file.filename.rsplit(".", 1)[1].lower()
        filename = secure_filename(f"{username}_profile.{ext}")
        save_path = os.path.join(PROFILE_PICS, filename)
        file.save(save_path)
        url = f"/static/uploads/profile_pics/{filename}"

        # Update DB if available
        if update_profile_pic:
            try:
                update_profile_pic(username, url)
            except Exception:
                pass

        # Update JSON fallback
        user = ensure_default_user(username)
        user["profile_pic"] = url
        save_user_to_json(username, user)

        return jsonify({"success": True, "url": url})
    return jsonify({"success": False}), 400


# ---------- Cover Pic Upload ----------
@profile_bp.route("/profile/upload_cover", methods=["POST"])
def upload_cover():
    if "user" not in session:
        return jsonify({"success": False, "message": "Login required"}), 401

    username = session["user"]
    file = request.files.get("file")
    if file and allowed_file(file.filename, ALLOWED_IMG):
        ext = file.filename.rsplit(".", 1)[1].lower()
        filename = secure_filename(f"{username}_cover.{ext}")
        save_path = os.path.join(COVER_PICS, filename)
        file.save(save_path)
        url = f"/static/uploads/cover_pics/{filename}"

        # Update DB if available
        if update_cover_pic:
            try:
                update_cover_pic(username, url)
            except Exception:
                pass

        # Update JSON fallback
        user = ensure_default_user(username)
        user["cover_pic"] = url
        save_user_to_json(username, user)

        return jsonify({"success": True, "url": url})
    return jsonify({"success": False}), 400


# ---------- Profile Page ----------
@profile_bp.route("/profile", methods=["GET", "POST"])
def profile():
    if "user" not in session:
        return redirect(url_for("auth.login"))

    username = session["user"]
    user = ensure_default_user(username)

    try:
        user["roadmap_progress"] = get_user_roadmap_progress(username)
    except Exception:
        user["roadmap_progress"] = user.get("roadmap_progress", 0)

    if request.method == "POST":
        # (same form handling as your code)
        # ... skipped for brevity ...
        # Save user JSON or DB
        if update_profile:
            try:
                update_profile(username, user)
            except Exception:
                save_user_to_json(username, user)
        else:
            save_user_to_json(username, user)

        flash("Profile saved", "success")
        return redirect(url_for("profile.profile"))

    return render_template("profile.html", user=user)


# ---------- Resume Download ----------
@profile_bp.route("/profile/download_resume/<username>")
def download_resume(username):
    if "user" not in session:
        return redirect(url_for("auth.login"))
    target_user = ensure_default_user(username)
    resume_path = target_user.get("resume", "")
    if not resume_path:
        flash("No resume uploaded.", "warning")
        return redirect(url_for("profile.profile"))

    filename = os.path.basename(resume_path)
    return send_from_directory(RESUMES_DIR, filename, as_attachment=True)


# ---------- Job Save ----------
@profile_bp.route("/profile/save_job", methods=["POST"])
def save_job():
    if "user" not in session:
        return jsonify({"success": False, "message": "Login required"}), 401
    username = session["user"]
    user = ensure_default_user(username)
    job_title = request.form.get("job_title") or (
        request.json.get("job_title") if request.is_json else None
    )
    if job_title and job_title not in user.get("saved_jobs", []):
        user.setdefault("saved_jobs", []).append(job_title)
        save_user_to_json(username, user)
    return jsonify({"success": True, "saved_jobs": user.get("saved_jobs", [])})


# ---------- Job Apply ----------
@profile_bp.route("/profile/apply_job", methods=["POST"])
def apply_job():
    if "user" not in session:
        return jsonify({"success": False, "message": "Login required"}), 401
    username = session["user"]
    user = ensure_default_user(username)
    job_title = request.form.get("job_title") or (
        request.json.get("job_title") if request.is_json else None
    )
    if job_title and job_title not in user.get("applied_jobs", []):
        user.setdefault("applied_jobs", []).append(job_title)
        save_user_to_json(username, user)
    return jsonify({"success": True, "applied_jobs": user.get("applied_jobs", [])})
