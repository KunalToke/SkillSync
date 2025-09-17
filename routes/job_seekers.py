from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for

# ---------- Blueprint ----------
job_seekers_bp = Blueprint(
    "job_seekers",
    __name__,
    template_folder='../templates'
)

# ---------- DASHBOARD ----------
@job_seekers_bp.route("/dashboard")
def dashboard():
    """
    Job Seeker Dashboard
    Make sure 'dashboard_jobseeker.html' exists in templates/job_seekers/
    """
    if "user" not in session:
        return redirect(url_for("auth.login"))  # Redirect to login if not logged in
    return render_template("dashboard_jobseekers.html", username=session.get("user"))

# ---------- CHATBOT ----------
@job_seekers_bp.route("/chatbot")
def chatbot():
    """
    Initialize chatbot session
    """
    session["chatbot_answers"] = []  # Reset session at start
    return render_template("chatbot.html")

@job_seekers_bp.route("/chatbot-answer", methods=["POST"])
def chatbot_answer():
    """
    Store each chatbot answer in session
    """
    answer = request.json.get("answer", "")
    if "chatbot_answers" not in session:
        session["chatbot_answers"] = []
    session["chatbot_answers"].append(answer)
    session.modified = True
    return jsonify(success=True)

# ---------- VIEW CHATBOT ANSWERS ----------
@job_seekers_bp.route("/chatbot-answers")
def chatbot_answers():
    """
    Return all chatbot answers in JSON
    """
    answers = session.get("chatbot_answers", [])
    return jsonify(answers=answers)
