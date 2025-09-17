from flask import Blueprint, render_template, session, redirect, url_for, request

employer_bp = Blueprint('employer', __name__, template_folder='../templates')

# Dummy storage for example
company_profiles = []
posted_jobs = []

@employer_bp.route('/company-profile', methods=['GET', 'POST'])
def company_profile():
    if "user" not in session:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        company_name = request.form.get('company_name')
        description = request.form.get('description')
        company_profiles.append({'company_name': company_name, 'description': description})
        message = "Company profile saved!"
        return render_template('company_profile.html', profiles=company_profiles, message=message)

    return render_template('company_profile.html', profiles=company_profiles)

@employer_bp.route('/post-job', methods=['GET', 'POST'])
def post_job():
    if "user" not in session:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        title = request.form.get('title')
        skills = request.form.get('skills')
        location = request.form.get('location')
        salary = request.form.get('salary')
        posted_jobs.append({'title': title, 'skills': skills, 'location': location, 'salary': salary})
        message = "Job posted successfully!"
        return render_template('post_job.html', jobs=posted_jobs, message=message)

    return render_template('post_job.html', jobs=posted_jobs)

@employer_bp.route('/search-candidates')
def search_candidates():
    if "user" not in session:
        return redirect(url_for('auth.login'))
    return render_template('search_candidates.html')

@employer_bp.route('/applications')
def applications():
    if "user" not in session:
        return redirect(url_for('auth.login'))
    return render_template('applications.html')
