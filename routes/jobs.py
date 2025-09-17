from flask import Blueprint, render_template, request, session, redirect, url_for
from models.jobs import job_alerts   # import jobs data

jobs_bp = Blueprint('jobs', __name__, template_folder='../templates')

@jobs_bp.route('/jobs', methods=["GET"])
def jobs():
    if "user" not in session:
        return redirect(url_for('auth.login'))

    search = request.args.get("search", "").lower()
    category_filter = request.args.get("category", "")

    filtered_jobs = []
    for job in job_alerts:
        if category_filter and job["category"] != category_filter:
            continue
        if search and search not in job["title"].lower() and search not in job["company"].lower():
            continue
        filtered_jobs.append(job)

    return render_template(
        "jobs.html",
        jobs=filtered_jobs,
        categories=sorted(set(j["category"] for j in job_alerts))
    )
@career_path_bp.route("/jobs")
def job_search():
    jobs = [
        # --- AI & ML ---
        {"title": "AI Engineer", "company": "Microsoft", "location": "Bangalore, India", "link": "https://careers.microsoft.com/"},
        {"title": "Machine Learning Engineer", "company": "Google", "location": "Hyderabad, India", "link": "https://careers.google.com/"},
        {"title": "Data Scientist", "company": "Amazon", "location": "Chennai, India", "link": "https://www.amazon.jobs/"},
        {"title": "NLP Engineer", "company": "OpenAI", "location": "Remote", "link": "https://openai.com/careers"},
        {"title": "Computer Vision Engineer", "company": "Tesla", "location": "California, USA", "link": "https://www.tesla.com/careers"},

        # --- Web Development ---
        {"title": "Frontend Developer", "company": "Adobe", "location": "Noida, India", "link": "https://adobe.wd5.myworkdayjobs.com/en-US/external_experienced"},
        {"title": "Backend Developer", "company": "Flipkart", "location": "Bangalore, India", "link": "https://www.flipkartcareers.com/"},
        {"title": "Full-Stack Developer", "company": "Zoho", "location": "Chennai, India", "link": "https://careers.zohocorp.com/"},
        {"title": "Web Developer", "company": "Infosys", "location": "Pune, India", "link": "https://www.infosys.com/careers"},
        {"title": "Mobile App Developer", "company": "Swiggy", "location": "Bangalore, India", "link": "https://careers.swiggy.com/"},

        # --- Cloud & DevOps ---
        {"title": "Cloud Engineer", "company": "AWS", "location": "Remote", "link": "https://aws.amazon.com/careers/"},
        {"title": "DevOps Engineer", "company": "Google Cloud", "location": "Hyderabad, India", "link": "https://careers.google.com/"},
        {"title": "Site Reliability Engineer", "company": "Netflix", "location": "California, USA", "link": "https://jobs.netflix.com/"},
        {"title": "Cloud Security Engineer", "company": "Oracle", "location": "Bangalore, India", "link": "https://www.oracle.com/in/corporate/careers/"},
        {"title": "Systems Administrator", "company": "Wipro", "location": "Pune, India", "link": "https://careers.wipro.com/"},

        # --- Cybersecurity ---
        {"title": "Ethical Hacker", "company": "Cisco", "location": "Bangalore, India", "link": "https://jobs.cisco.com/"},
        {"title": "Security Analyst", "company": "IBM", "location": "Noida, India", "link": "https://www.ibm.com/careers/in-en/"},
        {"title": "Incident Response Analyst", "company": "Accenture", "location": "Mumbai, India", "link": "https://www.accenture.com/in-en/careers"},
        {"title": "Network Security Engineer", "company": "HCL", "location": "Chennai, India", "link": "https://www.hcltech.com/careers"},
        {"title": "Digital Forensics Analyst", "company": "EY", "location": "Delhi, India", "link": "https://careers.ey.com/"},

        # --- Business & Management ---
        {"title": "Product Manager", "company": "Paytm", "location": "Noida, India", "link": "https://paytm.com/careers"},
        {"title": "Business Analyst", "company": "KPMG", "location": "Mumbai, India", "link": "https://kpmg.com/in/en/home/careers.html"},
        {"title": "Scrum Master", "company": "Capgemini", "location": "Pune, India", "link": "https://www.capgemini.com/careers/"},
        {"title": "Finance Analyst", "company": "JP Morgan", "location": "Delhi, India", "link": "https://careers.jpmorgan.com/"},
        {"title": "Entrepreneurship Program Associate", "company": "Startup India", "location": "Remote", "link": "https://www.startupindia.gov.in/"},

        # --- Design ---
        {"title": "UI/UX Designer", "company": "Canva", "location": "Sydney, Australia", "link": "https://www.canva.com/careers/"},
        {"title": "Product Designer", "company": "Figma", "location": "Remote", "link": "https://www.figma.com/careers/"},
        {"title": "Graphic Designer", "company": "Byju’s", "location": "Bangalore, India", "link": "https://byjus.com/careers/"},
        {"title": "Motion Graphics Artist", "company": "Disney", "location": "California, USA", "link": "https://jobs.disneycareers.com/"},
        {"title": "Animation Designer", "company": "Pixar", "location": "California, USA", "link": "https://pixar.wd5.myworkdayjobs.com/en-US/PixarCareerSite"},

        # --- Emerging Tech ---
        {"title": "Blockchain Developer", "company": "Polygon", "location": "Remote", "link": "https://polygon.technology/careers"},
        {"title": "Web3 Developer", "company": "Coinbase", "location": "Remote", "link": "https://www.coinbase.com/careers"},
        {"title": "IoT Engineer", "company": "Bosch", "location": "Bangalore, India", "link": "https://www.bosch.in/careers/"},
        {"title": "Robotics Engineer", "company": "Boston Dynamics", "location": "USA", "link": "https://bostondynamics.com/careers"},
        {"title": "Quantum Computing Researcher", "company": "IBM Research", "location": "Zurich, Switzerland", "link": "https://www.research.ibm.com/careers"},
        {"title": "Autonomous Vehicle Engineer", "company": "Waymo", "location": "California, USA", "link": "https://waymo.com/careers"},
    ]

    return render_template("career_path/job_search.html", jobs=jobs)
