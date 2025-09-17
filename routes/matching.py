from flask import Blueprint, render_template, session, redirect, url_for, request, flash

matching_bp = Blueprint('matching', __name__, template_folder='../templates')

# 🔹 Extended Job List with Apply Links
jobs = [
    {'id': 1, 'title': 'Python Developer', 'company': 'TechSoft',
     'skills': 'Python, Django, Flask', 'location': 'Remote', 'type': 'Full-time',
     'experience': '1-3 Years',
     'description': 'Work on backend APIs and scalable systems.',
     'apply_link': 'mailto:hr@techsoft.com'},

    {'id': 2, 'title': 'Data Analyst', 'company': 'DataWorks',
     'skills': 'SQL, Excel, Python', 'location': 'Bangalore', 'type': 'Full-time',
     'experience': 'Fresher',
     'description': 'Analyze business data and prepare reports.',
     'apply_link': 'https://careers.dataworks.com/apply/data-analyst'},

    {'id': 3, 'title': 'ML Engineer', 'company': 'AI Labs',
     'skills': 'Python, ML, TensorFlow, PyTorch', 'location': 'Mumbai', 'type': 'Full-time',
     'experience': '3-5 Years',
     'description': 'Build and deploy ML/AI models for production.',
     'apply_link': 'mailto:jobs@ailabs.com'},

    {'id': 4, 'title': 'Frontend Developer', 'company': 'Webify',
     'skills': 'JavaScript, React, CSS', 'location': 'Remote', 'type': 'Part-time',
     'experience': '1-3 Years',
     'description': 'Develop UI features and maintain web apps.',
     'apply_link': 'https://webify.in/careers/frontend'},

    {'id': 5, 'title': 'Finance Analyst', 'company': 'FinCorp',
     'skills': 'Finance, Excel, SQL', 'location': 'Delhi', 'type': 'Full-time',
     'experience': '1-3 Years',
     'description': 'Work on financial modeling and investment reports.',
     'apply_link': 'mailto:careers@fincorp.com'},
]


# 🔹 Job Search
@matching_bp.route('/jobs', methods=['GET'])
def match_jobs():
    if "user" not in session:
        return redirect(url_for('auth.login'))

    # Get search parameters
    keyword = request.args.get('keyword', '').lower()
    location = request.args.get('location', '').lower()
    job_type = request.args.get('type', '').lower()
    experience = request.args.get('experience', '').lower()

    # Filter jobs
    filtered_jobs = jobs
    if keyword:
        filtered_jobs = [job for job in filtered_jobs
                         if keyword in job['title'].lower() or keyword in job['skills'].lower()]
    if location:
        filtered_jobs = [job for job in filtered_jobs if location in job['location'].lower()]
    if job_type:
        filtered_jobs = [job for job in filtered_jobs if job_type in job['type'].lower()]
    if experience:
        filtered_jobs = [job for job in filtered_jobs if experience in job['experience'].lower()]

    return render_template('job_search.html', jobs=filtered_jobs)


# 🔹 Save Job
@matching_bp.route('/save_job/<int:job_id>')
def save_job(job_id):
    if "user" not in session:
        return redirect(url_for('auth.login'))

    if "saved_jobs" not in session:
        session["saved_jobs"] = []

    job = next((j for j in jobs if j['id'] == job_id), None)

    if job and job not in session["saved_jobs"]:
        session["saved_jobs"].append(job)
        session.modified = True
        flash("✅ Job saved successfully!", "success")
    else:
        flash("⚠️ Job already saved or not found!", "warning")

    return redirect(url_for('matching.match_jobs'))


# 🔹 View Saved Jobs
@matching_bp.route('/saved_jobs')
def saved_jobs():
    if "user" not in session:
        return redirect(url_for('auth.login'))

    saved = session.get("saved_jobs", [])
    return render_template("saved_jobs.html", jobs=saved)


# 🔹 Remove Saved Job
@matching_bp.route('/remove_job/<int:job_id>')
def remove_job(job_id):
    if "user" not in session:
        return redirect(url_for('auth.login'))

    if "saved_jobs" in session:
        session["saved_jobs"] = [j for j in session["saved_jobs"] if j['id'] != job_id]
        session.modified = True
        flash("🗑️ Job removed from saved jobs", "info")

    return redirect(url_for('matching.saved_jobs'))


# 🔹 Apply Job → moves from Saved → Applied
@matching_bp.route('/apply_job/<int:job_id>')
def apply_job(job_id):
    if "user" not in session:
        return redirect(url_for('auth.login'))

    if "applied_jobs" not in session:
        session["applied_jobs"] = []

    # Find the job
    job = next((j for j in jobs if j['id'] == job_id), None)

    if job:
        # Add default status if not present
        if "status" not in job:
            job["status"] = "Pending"

        # Remove from saved jobs if present
        if "saved_jobs" in session:
            session["saved_jobs"] = [j for j in session["saved_jobs"] if j['id'] != job_id]

        # Add to applied jobs
        if job not in session["applied_jobs"]:
            session["applied_jobs"].append(job)
            session.modified = True
            flash("🚀 Job moved to Applied Jobs! (Status: Pending)", "success")
        else:
            flash("⚠️ Already applied to this job!", "warning")

    # 👉 Redirect to applied jobs page (not external link)
    return redirect(url_for('matching.applied_jobs'))


# 🔹 View Applied Jobs
@matching_bp.route('/applied_jobs')
def applied_jobs():
    if "user" not in session:
        return redirect(url_for('auth.login'))

    applied = session.get("applied_jobs", [])
    return render_template("applied_jobs.html", jobs=applied)


# 🔹 Step 3: Update Application Status
@matching_bp.route('/update_status/<int:job_id>', methods=['POST'])
def update_status(job_id):
    if "user" not in session:
        return redirect(url_for('auth.login'))

    new_status = request.form.get("status")
    if "applied_jobs" in session:
        for job in session["applied_jobs"]:
            if job["id"] == job_id:
                job["status"] = new_status
                session.modified = True
                flash(f"📌 Status updated to {new_status}", "info")
                break

    return redirect(url_for('matching.applied_jobs'))
