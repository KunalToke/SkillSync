from flask import Blueprint, render_template, request, session, redirect, url_for
from models.jobs import jobs_by_company

alerts_bp = Blueprint("alerts", __name__, template_folder="../templates")

@alerts_bp.route("/alerts")
def alerts():
    if "user" not in session:
        return redirect(url_for("auth.login"))

    search = request.args.get("search", "").lower()
    company_filter = request.args.get("company", "")
    location_filter = request.args.get("location", "")

    filtered_jobs = {}

    for company, job_list in jobs_by_company.items():
        # ✅ apply company filter
        if company_filter and company != company_filter:
            continue

        # ✅ apply search + location filters
        results = []
        for job in job_list:
            if search and search not in job["title"].lower():
                continue
            if location_filter and job["location"] != location_filter:
                continue
            results.append(job)

        if results:
            filtered_jobs[company] = results

    return render_template("alerts.html", jobs_by_company=filtered_jobs)
