# routes/job_search.py
from flask import Blueprint, render_template, request
import math

job_search_bp = Blueprint('job_search', __name__)

# --- Example jobs dataset (replace/extend with DB or API) ---
ALL_JOBS = [
    {"title": "AI Engineer", "company": "Google", "location": "Bangalore", "link": "https://careers.google.com/jobs/results/123-ai"},
    {"title": "Data Scientist", "company": "Microsoft", "location": "Hyderabad", "link": "https://careers.microsoft.com/us/en/job/456-ds"},
    {"title": "Full-Stack Developer", "company": "Amazon", "location": "Pune", "link": "https://amazon.jobs/en/jobs/789-fsd"},
    {"title": "Cybersecurity Analyst", "company": "Deloitte", "location": "Mumbai", "link": "https://jobs.deloitte.com/cyber-analyst"},
    # ... add 100+ jobs ...
]

@job_search_bp.route("/job_search")
def job_search():
    page = int(request.args.get("page", 1))
    per_page = 12

    title = request.args.get("title", "").lower()
    company = request.args.get("company", "").lower()
    location = request.args.get("location", "").lower()

    # --- server-side filtering ---
    filtered = []
    for job in ALL_JOBS:
        if (title in job["title"].lower()) and \
           (company in job["company"].lower()) and \
           (location in job["location"].lower()):
            filtered.append(job)

    total = len(filtered)
    total_pages = math.ceil(total / per_page)
    start = (page - 1) * per_page
    end = start + per_page
    jobs = filtered[start:end]

    return render_template("career_path/job_search.html",
                           jobs=jobs,
                           page=page,
                           total_pages=total_pages,
                           title=title, company=company, location=location)
