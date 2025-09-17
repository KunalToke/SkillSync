from flask import Blueprint, render_template, request, redirect, url_for, session, make_response
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

career_path_bp = Blueprint('career_path', __name__)

# -------------------- Main Entry --------------------
@career_path_bp.route("/career_path")
def career_path():
    return render_template("career_path_guidance.html")

# -------------------- 1. Skill & Interest Assessment --------------------
@career_path_bp.route("/career_path/assessment", methods=["GET", "POST"])
def assessment():
    if request.method == "POST":
        answers = {}
        for i in range(1, 11):
            answers[f"q{i}"] = request.form.get(f"q{i}")
        session["quiz_results"] = answers
        return redirect(url_for("career_path.ai_recommendations"))
    return render_template("career_path/assessment.html")

# -------------------- 2. AI-Powered Recommendations --------------------
@career_path_bp.route("/career_path/ai_recommendations")
def ai_recommendations():
    quiz_results = session.get("quiz_results", {})
    suggestions, learning_paths = [], []

    if not quiz_results:
        return render_template("career_path/ai_recommendations.html", suggestions=None)

    # Expanded Rules
    if quiz_results.get("q1") == "coding":
        suggestions += ["Software Engineer", "AI Engineer", "Full Stack Developer", "Game Developer"]
        learning_paths += ["Python, C++, Data Structures, Cloud Computing"]
    if quiz_results.get("q1") == "design":
        suggestions += ["UI/UX Designer", "Graphic Designer", "Product Designer", "Motion Graphics Artist"]
        learning_paths += ["Figma, Adobe XD, Animation, User Psychology"]
    if quiz_results.get("q1") == "business":
        suggestions += ["Business Analyst", "Project Manager", "Entrepreneur", "Digital Marketer"]
        learning_paths += ["Agile, Finance, Growth Marketing, Leadership"]

    if quiz_results.get("q3") == "research":
        suggestions += ["AI Researcher", "Data Scientist", "PhD Scholar"]
    if quiz_results.get("q7") == "teaching":
        suggestions += ["Trainer", "Professor", "Corporate Coach"]

    return render_template("career_path/ai_recommendations.html",
                           suggestions=list(set(suggestions)),
                           learning_paths=list(set(learning_paths)))

# -------------------- 3. Job Market Insights --------------------
@career_path_bp.route("/career_path/job_market")
def job_market():
    insights = [
        {"role": "AI Engineer", "growth": "40% YoY", "avg_salary": "$120k"},
        {"role": "Cybersecurity Analyst", "growth": "35% YoY", "avg_salary": "$105k"},
        {"role": "Data Scientist", "growth": "30% YoY", "avg_salary": "$115k"},
        {"role": "UI/UX Designer", "growth": "25% YoY", "avg_salary": "$85k"},
        {"role": "Cloud Engineer", "growth": "28% YoY", "avg_salary": "$110k"},
        {"role": "Product Manager", "growth": "22% YoY", "avg_salary": "$130k"},
        {"role": "DevOps Engineer", "growth": "26% YoY", "avg_salary": "$108k"},
        {"role": "Digital Marketer", "growth": "18% YoY", "avg_salary": "$75k"},
        {"role": "Healthcare Data Analyst", "growth": "32% YoY", "avg_salary": "$95k"},
        {"role": "Blockchain Developer", "growth": "34% YoY", "avg_salary": "$125k"},
    ]
    return render_template("career_path/job_market.html", insights=insights)

# -------------------- 4. Skill Gap Analysis --------------------
@career_path_bp.route("/career_path/skill_gap")
def skill_gap():
    user_skills = ["Python", "SQL", "HTML"]  # Later: dynamic from user profile
    target_roles = {
        "AI Engineer": ["Python", "TensorFlow", "Deep Learning", "Cloud"],
        "Data Scientist": ["Python", "SQL", "Statistics", "Machine Learning", "Visualization"],
        "UI/UX Designer": ["Figma", "Prototyping", "User Research", "Usability Testing"],
        "Cybersecurity Analyst": ["Networking", "Linux", "Ethical Hacking", "Security Tools"],
    }

    gaps = {role: [s for s in skills if s not in user_skills]
            for role, skills in target_roles.items()}

    return render_template("career_path/skill_gap.html",
                           user_skills=user_skills, gaps=gaps)

# -------------------- 5. Upskilling --------------------
@career_path_bp.route("/career_path/upskilling")
def upskilling():
    resources = {
        "AI Engineer": ["Fast.ai", "DeepLearning.ai", "Google Cloud AI", "Stanford CS231n"],
        "Data Scientist": ["Kaggle", "Coursera ML", "Analytics Vidhya", "DataCamp"],
        "UI/UX Designer": ["Figma Community", "Interaction Design Foundation", "Adobe Behance"],
        "Cybersecurity Analyst": ["HackTheBox", "TryHackMe", "Offensive Security Labs"],
        "Cloud Engineer": ["AWS Training", "GCP Qwiklabs", "Azure Fundamentals"],
    }
    return render_template("career_path/upskilling.html", resources=resources)

# -------------------- 6. Roadmaps (Grouped & Interactive) --------------------
@career_path_bp.route("/career_path/roadmap")
def roadmap():
    roadmap_domains = {
        "AI & Data": {
            "AI Engineer": ["Month 1: Python & Math", "Month 2: ML Fundamentals", "Month 3: Deep Learning", "Month 4: Cloud AI", "Month 5–6: Projects"],
            "Machine Learning Engineer": ["Month 1: Python + Stats", "Month 2: ML Algorithms", "Month 3: MLOps", "Month 4–5: Deployments"],
            "Data Scientist": ["Month 1: SQL + Python", "Month 2: Statistics", "Month 3: ML Models", "Month 4: Big Data Tools", "Month 5–6: Deployments"],
            "AI Research Scientist": ["Month 1–2: Advanced Math", "Month 3: Deep Learning", "Month 4–5: Research Papers"],
            "NLP Engineer": ["Month 1: Python + NLTK", "Month 2: Transformers", "Month 3: Chatbots", "Month 4: Deploy NLP APIs"],
            "Computer Vision Engineer": ["Month 1: OpenCV", "Month 2: CNNs", "Month 3: Image Recognition", "Month 4: Real-Time Detection"],
            "Data Engineer": ["Month 1: ETL Basics", "Month 2: SQL + Spark", "Month 3: Data Pipelines", "Month 4: Cloud Data"],
        },
        "Web & Software": {
            "Front-End Developer": ["Week 1–2: HTML/CSS/JS", "Month 2: React", "Month 3: UI Frameworks"],
            "Back-End Developer": ["Month 1: Python/Node.js", "Month 2: Databases", "Month 3: APIs"],
            "Full-Stack Developer": ["Month 1: Frontend", "Month 2: Backend", "Month 3: Projects"],
            "Mobile App Developer": ["Month 1: Android/iOS", "Month 2: Flutter", "Month 3: Projects"],
            "Game Developer": ["Month 1: Unity/Unreal", "Month 2: Game Physics", "Month 3: Projects"],
            "Embedded Systems Engineer": ["Month 1: C/C++", "Month 2: Microcontrollers", "Month 3: IoT Integration"],
            "Software Architect": ["Month 1: Design Patterns", "Month 2: System Architecture"],
        },
        "Security": {
            "Ethical Hacker": ["Month 1: Networking", "Month 2: Kali Linux", "Month 3: PenTesting"],
            "Security Engineer": ["Month 1: Firewalls", "Month 2: IDS/IPS", "Month 3: Security Tools"],
            "Incident Response Analyst": ["Month 1: Threat Analysis", "Month 2: Incident Handling"],
            "Network Security Engineer": ["Month 1: TCP/IP", "Month 2: Firewalls", "Month 3: IDS"],
            "Cloud Security Specialist": ["Month 1: Cloud Basics", "Month 2: IAM & Security"],
            "Digital Forensics Analyst": ["Month 1: Disk Forensics", "Month 2: Malware Analysis"],
        },
        "Cloud & DevOps": {
            "DevOps Engineer": ["Month 1: Linux + Git", "Month 2: CI/CD", "Month 3: Docker/Kubernetes"],
            "Site Reliability Engineer": ["Month 1: Monitoring", "Month 2: Scaling", "Month 3: Automation"],
            "Cloud Architect": ["Month 1: AWS/Azure", "Month 2: Cloud Networking"],
            "Cloud Engineer": ["Month 1: Basics", "Month 2: Containers"],
            "Cloud Security Engineer": ["Month 1: IAM Policies", "Month 2: Threat Detection"],
            "Platform Engineer": ["Month 1: Infrastructure as Code", "Month 2: Orchestration"],
            "Systems Administrator": ["Month 1: Linux", "Month 2: Server Management"],
        },
        "Business & Management": {
            "Project Manager": ["Month 1: PM Basics", "Month 2: Agile", "Month 3: Leadership"],
            "Scrum Master": ["Month 1: Agile & Scrum", "Month 2: Team Coaching"],
            "Business Analyst": ["Month 1: Excel + SQL", "Month 2: Reports"],
            "Entrepreneurship": ["Month 1: Business Model", "Month 2: Funding"],
            "Digital Marketing Manager": ["Month 1: SEO", "Month 2: Social Media"],
            "AI Product Manager": ["Month 1: AI Basics", "Month 2: Product Strategy"],
        },
        "Design & Creative": {
            "UI/UX Designer": ["Month 1: Design Basics", "Month 2: Figma", "Month 3: Portfolio"],
            "Product Designer": ["Month 1: UX Design", "Month 2: Design Systems"],
        },
        "Emerging Tech": {
            "Blockchain Developer": ["Month 1: Solidity", "Month 2: Smart Contracts"],
            "Web3 Developer": ["Month 1: Ethereum", "Month 2: DApps"],
            "IoT Engineer": ["Month 1: Arduino/Raspberry Pi", "Month 2: IoT Security"],
            "Robotics Engineer": ["Month 1: Sensors", "Month 2: Motion Planning"],
            "Quantum Computing Researcher": ["Month 1: Qiskit Basics", "Month 2: Quantum Algorithms"],
            "AR/VR Developer": ["Month 1: Unity + ARKit/ARCore", "Month 2: Immersive Apps"],
            "Autonomous Vehicle Engineer": ["Month 1: Robotics", "Month 2: Self-Driving Algorithms"],
        },
    }

    return render_template("career_path/roadmap.html", roadmap_domains=roadmap_domains)

# -------------------- 7. Mentorship --------------------
@career_path_bp.route("/career_path/mentorship")
def mentorship():
    mentors = [
        {"name": "Alice", "field": "AI Engineer", "contact": "alice@example.com"},
        {"name": "Bob", "field": "Data Scientist", "contact": "bob@example.com"},
        {"name": "Charlie", "field": "UI/UX Designer", "contact": "charlie@example.com"},
        {"name": "David", "field": "Cybersecurity Analyst", "contact": "david@example.com"},
        {"name": "Eva", "field": "Cloud Engineer", "contact": "eva@example.com"},
    ]
    return render_template("career_path/mentorship.html", mentors=mentors)

# -------------------- 8. Transition --------------------
@career_path_bp.route("/career_path/transition")
def transition():
    transitions = {
        "Developer → Data Scientist": ["Learn Pandas", "Statistics", "ML"],
        "Designer → Product Manager": ["Learn Business Analytics", "Agile", "Leadership"],
        "SysAdmin → Cloud Engineer": ["AWS/GCP Certification", "DevOps", "Security"],
        "QA → DevOps": ["CI/CD", "Docker", "Kubernetes"],
        "Teacher → Instructional Designer": ["EdTech Tools", "Curriculum Design", "LMS"],
    }
    return render_template("career_path/transition.html", transitions=transitions)
# -------------------- Extra Code for Job Alert Page --------------------
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
# -------------------- Profile uodate page  --------------------
@career_path_bp.route("/profile")
def profile():
    # Example dummy user (later replace with DB data)
    user = {
        "name": "Sujal Vijay Sargar",
        "headline": "AI Engineer | Data Enthusiast",
        "location": "Pune, India",
        "relocation": "Open to relocation",
        "contact": "sujal@example.com",
        "profile_pic": "/static/images/profile.jpg",
        "cover_pic": "/static/images/cover.jpg",

        "about": "Passionate about AI/ML, data-driven decision making, and building impactful products.",
        "education": [
            {"school": "MIT University", "degree": "B.E. in AI & ML", "year": "2025"},
            {"school": "Coursera", "degree": "Deep Learning Specialization", "year": "2024"}
        ],
        "experience": [
            {"company": "Google Summer of Code", "role": "AI Intern", "year": "2024"},
            {"company": "StartupX", "role": "Data Analyst Intern", "year": "2023"}
        ],
        "skills": [
            {"name": "Python", "rating": 5},
            {"name": "Machine Learning", "rating": 4},
            {"name": "React", "rating": 3},
            {"name": "SQL", "rating": 4},
        ],
        "portfolio": {
            "github": "https://github.com/username",
            "linkedin": "https://linkedin.com/in/username",
            "behance": "https://behance.net/username"
        },
        "resume": "/static/resume/sujal_resume.pdf",

        # Career Growth
        "roadmap_progress": 65,
        "assessments": [
            {"test": "AI/ML Quiz", "score": "85%"},
            {"test": "Python Coding", "score": "90%"},
        ],
        "certificates": [
            {"name": "TensorFlow Developer", "year": "2024"},
            {"name": "AWS Cloud Practitioner", "year": "2023"}
        ],
        "job_preferences": {"role": "AI Engineer", "salary": "₹15 LPA", "remote": "Yes"},
        "saved_jobs": ["AI Engineer at Google", "Data Scientist at Amazon"],
        "applied_jobs": ["Machine Learning Engineer at Microsoft"],
        "recommendations": ["Alice: 'Great collaborator in AI projects.'"],

        # Interactive
        "endorsements": [
            {"skill": "Python", "endorsed_by": "John"},
            {"skill": "Machine Learning", "endorsed_by": "Alice"}
        ],
        "timeline": [
            {"year": "2023", "event": "Started B.E. in AI/ML"},
            {"year": "2024", "event": "Completed Deep Learning Specialization"},
            {"year": "2025", "event": "Interned at Google"},
        ],
        "achievements": [
            "Completed Data Science Bootcamp",
            "Won Hackathon at MIT Pune"
        ]
    }

    return render_template("profile.html", user=user)




# -------------------- 9. Download Roadmap as PDF --------------------
@career_path_bp.route("/career_path/download_pdf/<career>")
def download_pdf(career):
    # Simplified roadmap set, reuse from route above
    all_roadmaps = {
        "AI Engineer": ["Month 1: Python & Math", "Month 2: ML Fundamentals", "Month 3: Deep Learning", "Month 4: Cloud AI", "Month 5–6: Projects"],
        "Data Scientist": ["Month 1: SQL + Python", "Month 2: Statistics", "Month 3: ML Models", "Month 4: Big Data Tools", "Month 5–6: Deployments"],
        "DevOps Engineer": ["Month 1: Linux + Git", "Month 2: CI/CD", "Month 3: Docker/Kubernetes"],
        "UI/UX Designer": ["Month 1: Design Basics", "Month 2: Figma", "Month 3: Portfolio"],
        # add more as needed...
    }

    steps = all_roadmaps.get(career.replace("_", " "), ["No roadmap found."])

    # Create PDF
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, 750, f"{career} Roadmap")
    c.setFont("Helvetica", 12)

    y = 720
    for idx, step in enumerate(steps, start=1):
        c.drawString(50, y, f"Step {idx}: {step}")
        y -= 20
        if y < 50:
            c.showPage()
            y = 750
            c.setFont("Helvetica", 12)

    c.save()
    buffer.seek(0)

    response = make_response(buffer.read())
    response.headers["Content-Disposition"] = f"attachment; filename={career}_roadmap.pdf"
    response.headers["Content-Type"] = "application/pdf"
    return response
