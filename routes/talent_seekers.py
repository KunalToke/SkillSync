from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
import os
import random
from datetime import datetime

# ----------------- BLUEPRINT -----------------
talent_seekers_bp = Blueprint(
    "talent_seekers",
    __name__,
    template_folder='../templates' 
)

# ----------------- DEMO STORAGE -----------------
fit_reports = {
    "John Doe": {"match": 87, "strengths": ["Python (5+ yrs)", "Problem Solving"], "gaps": ["AWS"]},
    "Jane Smith": {"match": 72, "strengths": ["Java", "Leadership"], "gaps": ["Cloud"]}
}

uploaded_videos = []
jobs = []
job_counter = 1  # ensures jobs get unique IDs

applications_feed = [
    {"candidate": "Alex Johnson", "job": "Python Developer", "status": "Applied"},
    {"candidate": "Maria Garcia", "job": "UI/UX Designer", "status": "Interview Scheduled"},
    {"candidate": "Sam Lee", "job": "Data Scientist", "status": "Shortlisted"}
]

top_matches = [
    {"name": "John Doe", "match": 92, "skills": "Python, Django"},
    {"name": "Jane Smith", "match": 88, "skills": "Java, Spring"},
    {"name": "Alex Johnson", "match": 85, "skills": "UI/UX, Figma"}
]

hiring_pipeline = {
    "Applied": ["John Doe", "Maria Garcia"],
    "Shortlisted": ["Jane Smith"],
    "Interview": ["Alex Johnson"],
    "Hired": []
}

analytics_data = {
    "total_jobs": 12,
    "total_candidates": 48,
    "applications_received": 132,
    "avg_match_score": 81
}

tasks = [
    {"task": "Review John Doe's application", "due": "Today"},
    {"task": "Schedule interview with Maria Garcia", "due": "Tomorrow"},
    {"task": "Post new Backend Developer job", "due": "Next Week"}
]

market_insights = [
    {"trend": "High demand for AI Engineers (+25%)"},
    {"trend": "Remote roles increased by 40%"},
    {"trend": "UI/UX salaries growing by 15% YoY"}
]

# ----------------- APPLICATIONS DEMO DATA -----------------
applications_data = [
    {
        "id": 1,
        "candidate": "John Doe",
        "job_id": None,
        "job_title": "Python Developer",
        "status": "Applied",
        "applied_date": "2025-09-11T09:30:00",
        "match_score": 87,
        "skills": "Python, Django, SQL",
        "tests_completed": False,
        "duplicates": False,
        "notes": [{"author": "hr1", "time": "2025-09-11T10:00:00.000", "text": "Strong on algorithms."}],
        "timeline": [
            {"time": "2025-09-11T09:30:00.000", "event": "Applied"},
            {"time": "2025-09-12T14:00:00.000", "event": "Shortlisted"}
        ],
        "ai_score": 87,
        "portfolio": "https://github.com/johndoe",
        "comm_score": 78,
        "offer_prediction": 72,
        "nudge": False
    },
    {
        "id": 2,
        "candidate": "Jane Smith",
        "job_id": None,
        "job_title": "UI/UX Designer",
        "status": "Shortlisted",
        "applied_date": "2025-09-10T11:20:00",
        "match_score": 75,
        "skills": "Figma, UX, Prototyping",
        "tests_completed": True,
        "duplicates": True,
        "notes": [],
        "timeline": [
            {"time": "2025-09-10T11:20:00.000", "event": "Applied"},
            {"time": "2025-09-12T09:00:00.000", "event": "Shortlisted"},
            {"time": "2025-09-14T13:00:00.000", "event": "Interview scheduled"}
        ],
        "ai_score": 75,
        "portfolio": "https://linkedin.com/in/janesmith",
        "comm_score": 82,
        "offer_prediction": 53,
        "nudge": True
    },
    {
        "id": 3,
        "candidate": "Alex Johnson",
        "job_id": None,
        "job_title": "Data Scientist",
        "status": "Interview",
        "applied_date": "2025-09-09T08:45:00",
        "match_score": 82,
        "skills": "Pandas, ML, Python",
        "tests_completed": True,
        "duplicates": False,
        "notes": [{"author": "hr2", "time": "2025-09-10T12:00:00.000", "text": "Portfolio is great."}],
        "timeline": [
            {"time": "2025-09-09T08:45:00.000", "event": "Applied"},
            {"time": "2025-09-10T11:00:00.000", "event": "Shortlisted"},
            {"time": "2025-09-11T15:00:00.000", "event": "Interview"}
        ],
        "ai_score": 82,
        "portfolio": "https://behance.net/alexjohnson",
        "comm_score": 90,
        "offer_prediction": 81,
        "nudge": False
    }
]

def find_application_by_id(app_id):
    for a in applications_data:
        if a["id"] == app_id:
            return a
    return None

# ----------------- DASHBOARD -----------------
@talent_seekers_bp.route("/talent-seekers/dashboard")
def dashboard():
    return render_template(
        "talent_seekers/dashboard.html",
        stats=analytics_data,
        applications=applications_feed,
        matches=top_matches,
        pipeline=hiring_pipeline,
        tasks=tasks,
        market=market_insights
    )

# ----------------- FIT REPORT -----------------
@talent_seekers_bp.route("/talent-seekers/fit-report/<candidate>")
def fit_report(candidate):
    report = fit_reports.get(candidate, None)
    return render_template("talent_seekers/fit_report.html", candidate=candidate, report=report)

# ----------------- VIDEO SCREENING -----------------
@talent_seekers_bp.route("/talent-seekers/upload-video", methods=["GET", "POST"])
def upload_video():
    if request.method == "POST":
        file = request.files.get("video")
        if file:
            save_path = os.path.join("static/uploads/videos", file.filename)
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            file.save(save_path)
            uploaded_videos.append(file.filename)
            flash("Video uploaded successfully!", "success")
            return redirect(url_for("talent_seekers.view_videos"))
    return render_template("talent_seekers/upload_video.html")

@talent_seekers_bp.route("/talent-seekers/view-videos")
def view_videos():
    return render_template("talent_seekers/view_videos.html", videos=uploaded_videos)

# ----------------- TALENT POOLS -----------------
@talent_seekers_bp.route("/talent-seekers/talent-pools")
def talent_pools():
    pools = {"Data Science Talent": ["John Doe"], "Design Interns": ["Jane Smith"]}
    return render_template("talent_seekers/talent_pools.html", pools=pools)

# ----------------- CANDIDATE ENGAGEMENT -----------------
#@talent_seekers_bp.route("/talent-seekers/engagement")
#def engagement():
  #  engagement_data = {
 #      "Applications Completed": 60,
  #      "Interview Attendance": 40
   # }
    #return render_template("talent_seekers/engagement.html", engagement=engagement_data)

# ----------------- JOB MANAGEMENT -----------------
@talent_seekers_bp.route("/talent-seekers/post-job", methods=["GET", "POST"])
def post_job():
    global job_counter
    if request.method == "POST":
        title = request.form.get("title")
        skills = request.form.get("skills")
        location = request.form.get("location")
        salary = request.form.get("salary")
        openings = request.form.get("openings")

        if title and skills and location and salary and openings:
            jobs.append({
                "id": job_counter,
                "title": title,
                "skills": skills,
                "location": location,
                "salary": salary,
                "openings": int(openings)
            })
            job_counter += 1
            flash("Job posted successfully!", "success")
            return redirect(url_for("talent_seekers.post_job"))

    return render_template("talent_seekers/post_job.html", jobs=jobs)

@talent_seekers_bp.route("/talent-seekers/delete-job/<int:job_id>", methods=["POST"])
def delete_job(job_id):
    global jobs
    jobs = [job for job in jobs if job["id"] != job_id]
    flash("Job deleted successfully!", "danger")
    return redirect(url_for("talent_seekers.post_job"))

@talent_seekers_bp.route("/talent-seekers/edit-job/<int:job_id>", methods=["GET", "POST"])
def edit_job(job_id):
    for job in jobs:
        if job["id"] == job_id:
            if request.method == "POST":
                job["title"] = request.form.get("title")
                job["skills"] = request.form.get("skills")
                job["location"] = request.form.get("location")
                job["salary"] = request.form.get("salary")
                job["openings"] = int(request.form.get("openings", job.get("openings", 1)))
                flash("Job updated successfully!", "info")
                return redirect(url_for("talent_seekers.post_job"))
            return render_template("talent_seekers/edit_job.html", job=job)
    flash("Job not found!", "warning")
    return redirect(url_for("talent_seekers.post_job"))

# ----------------- APPLICATIONS -----------------
@talent_seekers_bp.route("/talent-seekers/applications")
def applications():
    return render_template(
        "talent_seekers/applications.html",
        applications=applications_data,
        pipeline=hiring_pipeline,
        jobs=jobs,
        now=datetime.utcnow().isoformat()
    )

@talent_seekers_bp.route("/talent-seekers/nudge/<int:app_id>", methods=["POST"])
def nudge(app_id):
    app = find_application_by_id(app_id)
    if not app:
        return jsonify({"success": False, "message": "Application not found"}), 404
    app["nudge"] = True
    app.setdefault("notes", []).append({"author": "system", "time": datetime.utcnow().isoformat(), "text": "Nudge sent to candidate."})
    return jsonify({"success": True, "message": f"Nudge sent to {app['candidate']}."})

@talent_seekers_bp.route("/talent-seekers/mark-tested/<int:app_id>", methods=["POST"])
def mark_tested(app_id):
    app = find_application_by_id(app_id)
    if not app:
        return jsonify({"success": False, "message": "Application not found"}), 404
    app["tests_completed"] = True
    app.setdefault("notes", []).append({"author":"system","time":datetime.utcnow().isoformat(),"text":"Tests marked completed by recruiter."})
    return jsonify({"success": True, "message": "Marked tests completed."})

@talent_seekers_bp.route("/talent-seekers/timeline/<int:app_id>")
def timeline(app_id):
    app = find_application_by_id(app_id)
    if not app:
        return jsonify({"success": False, "message": "Application not found"}), 404
    return jsonify({"success": True, "timeline": app.get("timeline", [])})

@talent_seekers_bp.route("/talent-seekers/add-feedback", methods=["POST"])
def add_feedback():
    app_id = request.form.get("app_id", type=int)
    author = request.form.get("author", "anonymous")
    text = request.form.get("text", "")
    app = find_application_by_id(app_id)
    if not app:
        flash("Application not found", "warning")
        return redirect(url_for("talent_seekers.applications"))
    app.setdefault("notes", []).append({"author": author, "time": datetime.utcnow().isoformat(), "text": text})
    flash("Feedback saved", "success")
    return redirect(url_for("talent_seekers.applications"))

# ----------------- AUTOMATION -----------------
@talent_seekers_bp.route("/talent-seekers/automation")
def automation():
    return render_template("talent_seekers/automation.html")


# ----------------- Resume Shortlister -----------------
@talent_seekers_bp.route("/talent-seekers/resume-shortlister", methods=["POST"])
def resume_shortlister():
    file = request.files.get("resume")
    if not file:
        flash("No file uploaded!", "danger")
        return redirect(url_for("talent_seekers.automation"))

    filename = file.filename
    candidate_name = filename.rsplit(".", 1)[0].replace("_", " ").title()

    matched_candidate = None
    for app in applications_data:
        if app["candidate"].lower() == candidate_name.lower():
            matched_candidate = app
            break

    if matched_candidate:
        shortlist_score = matched_candidate["ai_score"]
        skills = matched_candidate["skills"]
        role = matched_candidate["job_title"]
        status = "Matched with existing candidate profile"
    else:
        # Random role + skills if not matched
        roles = ["Frontend Developer", "Backend Developer", "Data Scientist", "ML Engineer", "UI/UX Designer"]
        skills_pool = [
            "Python, Django, SQL", "Java, Spring Boot", "React, Node.js", 
            "Machine Learning, TensorFlow", "Figma, UI/UX"
        ]
        shortlist_score = random.randint(60, 95)
        role = random.choice(roles)
        skills = random.choice(skills_pool)
        status = "New candidate (AI estimated profile)"

    return render_template(
        "talent_seekers/resume_result.html",
        filename=filename,
        score=shortlist_score,
        skills=skills,
        role=role,
        status=status
    )


# ----------------- Auto-Ranking Candidates -----------------
@talent_seekers_bp.route("/talent-seekers/auto-ranking")
def auto_ranking():
    ranked_candidates = sorted(applications_data, key=lambda x: x["ai_score"], reverse=True)
    return render_template("talent_seekers/auto_ranking.html", candidates=ranked_candidates)


# ----------------- Chatbot Simulation -----------------
#@job_seekers_bp.route("/job-seekers/chatbot")
#def chatbot():
 #   session["chatbot_answers"] = []  # reset session at start
  #  return render_template("job_seekers/chatbot.html")


#@job_seekers_bp.route("/job-seekers/chatbot-answer", methods=["POST"])
#def chatbot_answer():
 #   answer = request.json.get("answer", "")
  #  if "chatbot_answers" not in session:
   #     session["chatbot_answers"] = []
    #session["chatbot_answers"].append(answer)
    #session.modified = True
    #return jsonify(success=True)


# ----------------- Show Chatbot Answers in Applications -----------------
@talent_seekers_bp.route("/talent-seekers/chatbot-answers")
def chatbot_answers():
    answers = session.get("chatbot_answers", [])
    return jsonify(answers=answers)



# ----------------- HIRING INSIGHTS -----------------
@talent_seekers_bp.route("/hiring-insights")
def hiring_insights():
    # Mock data for AI insights
    qhi = 85
    performance, retention, satisfaction = 80, 90, 85

    offer_acceptance = [
        {"role": "Frontend Developer", "prob": 78},
        {"role": "Data Scientist", "prob": 85},
        {"role": "UI/UX Designer", "prob": 65},
    ]

    heatmap_data = {
        "Engineering": [20, 25, 18, 30],
        "Data Science": [15, 20, 22, 28],
        "Design": [10, 15, 12, 18],
    }

    competitor_benchmark = [
        {"company": "TechCorp", "avg_hire_days": 25, "offer_acceptance": 80},
        {"company": "DataWorks", "avg_hire_days": 30, "offer_acceptance": 75},
        {"company": "DesignHub", "avg_hire_days": 28, "offer_acceptance": 70},
    ]

    funnel = {
        "Applied": 200,
        "Screened": 150,
        "Interviewed": 90,
        "Offered": 50,
        "Hired": 30,
    }

    budget_vs_outcomes = {
        "budget_allocated": 100000,
        "spent": 65000,
        "hires": 25,
    }

    pipeline_forecast = {
        "expected_hires_next_quarter": 40,
        "risk_level": "Medium",
        "critical_roles": ["ML Engineer", "Cloud Architect"],
    }

    diversity_index = 45  # % of diverse hires
    skill_gap = {"Python": 85,"Machine Learning": 70,"Data Visualization": 60,"Cloud Computing": 50,"Leadership": 40}
    attrition_risk = {"High": 15,"Medium": 25,"Low": 60}
    hiring_sources = [
        {"source": "LinkedIn", "hires": 20},
        {"source": "Referrals", "hires": 15},
        {"source": "Job Boards", "hires": 10},
        {"source": "Campus", "hires": 5},
    ]
    sentiment_score = 78
    trending_roles = ["AI Engineer", "Product Manager", "DevOps Specialist"]
    cost_per_hire = 4200

    return render_template("talent_seekers/hiring_insights.html",
                           qhi=qhi,performance=performance,retention=retention,satisfaction=satisfaction,
                           offer_acceptance=offer_acceptance,heatmap_data=heatmap_data,
                           competitor_benchmark=competitor_benchmark,funnel=funnel,
                           budget_vs_outcomes=budget_vs_outcomes,pipeline_forecast=pipeline_forecast,
                           diversity_index=diversity_index,skill_gap=skill_gap,attrition_risk=attrition_risk,
                           hiring_sources=hiring_sources,sentiment_score=sentiment_score,
                           trending_roles=trending_roles,cost_per_hire=cost_per_hire)

# ----------------- SEARCH CANDIDATES -----------------
@talent_seekers_bp.route("/talent-seekers/search-candidates")
def search_candidates():
    # Filters for dropdowns
    diversity_tags = ["Women in Tech","Veterans","LGBTQ+","Persons with Disabilities","First-Gen Graduate"]
    urgencies = ["Low","Medium","High"]
    skills_list = ["Python","Java","C++","JavaScript","React","Node.js","AI/ML","Data Science","Web Dev","UI/UX"]
    job_roles = ["Frontend Developer","Backend Developer","Full Stack Developer",
                 "Data Scientist","ML Engineer","UI/UX Designer","DevOps Engineer",
                 "Cloud Engineer","Software Engineer","Mobile App Developer"]

    query = request.args.get("q", "")
    filter_diversity = request.args.get("diversity", "")
    filter_urgency = request.args.get("urgency", "")
    filter_skill = request.args.get("skill", "")

    # --- Seed Candidates ---
    candidates = [
        {
            "name": "Aarav Sharma","role": "Data Scientist","experience": "2 years","location": "Mumbai",
            "ai_match": 92,"skills": "Python, Machine Learning, SQL",
            "soft_skills": ["Teamwork","Problem Solving"],
            "ai_highlight": "Built ML models with 90%+ accuracy in internships.",
            "github": "https://github.com/aaravsharma","linkedin": "https://linkedin.com/in/aaravsharma",
            "portfolio": None,"availability": "Immediate","urgency": "High","diversity": "First-Gen Graduate",
            "growth_index": "88%","peer_recs": ["Priya K.","Rohit M."],
            "gamified": {"level": 5,"badges": ["Fast Learner","Hackathon Winner"]},"video_resume": None
        },
        {
            "name": "Saanvi Patel","role": "Frontend Developer","experience": "3 years","location": "Bengaluru",
            "ai_match": 85,"skills": "Java, Spring Boot, React","soft_skills": ["Leadership","Communication"],
            "ai_highlight": "Led a 4-member team in a web app project.",
            "github": "https://github.com/saanvipatel","linkedin": "https://linkedin.com/in/saanvipatel",
            "portfolio": "https://saanvi.dev","availability": "2 Weeks","urgency": "Medium",
            "diversity": "Women in Tech","growth_index": "91%","peer_recs": ["Ananya R."],
            "gamified": {"level": 7,"badges": ["Innovator","Team Player"]},"video_resume": None
        }
    ]

    # --- Auto-generate More Candidates ---
    names = ["Ishita Rao","Aditya Gupta","Meera Nair","Rohan Desai","Ananya Iyer",
             "Arjun Kapoor","Tanvi Mehta","Raj Malhotra","Simran Khanna","Vikram Joshi"]
    for i, name in enumerate(names):
        candidates.append({
            "name": name,"role": random.choice(job_roles),"experience": f"{(i % 5) + 1} years",
            "location": f"City {(i % 10) + 1}","ai_match": 70 + (i % 30),
            "skills": f"{skills_list[i % len(skills_list)]}, SQL",
            "soft_skills": ["Communication","Adaptability","Problem Solving"],
            "ai_highlight": "Actively contributed to open-source projects.",
            "github": "https://github.com/example" if i % 2 == 0 else None,
            "linkedin": "https://linkedin.com/in/example" if i % 3 == 0 else None,
            "portfolio": "https://portfolio.example.com" if i % 4 == 0 else None,
            "availability": "Immediate" if i % 2 == 0 else "2 Weeks",
            "urgency": urgencies[i % len(urgencies)],"diversity": diversity_tags[i % len(diversity_tags)],
            "growth_index": f"{75 + (i % 20)}%","peer_recs": [f"Peer {j}" for j in range(1,(i % 3) + 2)],
            "gamified": {"level": (i % 10) + 1,"badges": ["Learner","Innovator"]},"video_resume": None
        })

    filtered_candidates = [
        c for c in candidates
        if (not query or query.lower() in c["name"].lower() or query.lower() in c["skills"].lower() or query.lower() in c.get("role", "").lower())
        and (not filter_diversity or c["diversity"] == filter_diversity)
        and (not filter_urgency or c["urgency"] == filter_urgency)
        and (not filter_skill or filter_skill in c["skills"])
    ]

    return render_template("talent_seekers/search_candidates.html",
                           candidates=filtered_candidates,query=query,
                           diversity_tags=diversity_tags,urgencies=urgencies,skills_list=skills_list,
                           filter_diversity=filter_diversity,filter_urgency=filter_urgency,filter_skill=filter_skill)
