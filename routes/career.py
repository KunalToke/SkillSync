from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from models.user import save_career, get_saved_careers, remove_saved_career, get_user_by_username

career_bp = Blueprint("career", __name__, url_prefix="/career")

# Example careers (static list for now) with unique IDs
career_list = [
    {
        "id": 1,
        "title": "Data Scientist",
        "description": "Analyze complex data sets to extract actionable insights and support business decisions.",
        "skills": "Python, Machine Learning, SQL, Statistics",
        "growth": "High",
        "salary": "$95,000 - $130,000"
    },
    {
        "id": 2,
        "title": "AI Engineer",
        "description": "Design and build AI-powered applications such as chatbots, recommendation systems, and automation tools.",
        "skills": "Deep Learning, TensorFlow, PyTorch, NLP",
        "growth": "High",
        "salary": "$100,000 - $140,000"
    },
    {
        "id": 3,
        "title": "Web Developer",
        "description": "Develop and maintain dynamic, user-friendly websites and web applications.",
        "skills": "HTML, CSS, JavaScript, React, Django/Flask",
        "growth": "Medium",
        "salary": "$65,000 - $90,000"
    },
    {
        "id": 4,
        "title": "Cloud Engineer",
        "description": "Manage and deploy scalable cloud infrastructure and services for enterprises.",
        "skills": "AWS, Azure, Google Cloud, Kubernetes, Docker",
        "growth": "High",
        "salary": "$95,000 - $125,000"
    },
    {
        "id": 5,
        "title": "Cybersecurity Analyst",
        "description": "Protect systems and networks from cyber threats, attacks, and vulnerabilities.",
        "skills": "Networking, Firewalls, Penetration Testing, SIEM",
        "growth": "High",
        "salary": "$85,000 - $115,000"
    },
    {
        "id": 6,
        "title": "Mobile App Developer",
        "description": "Create and optimize mobile applications for iOS and Android devices.",
        "skills": "Flutter, React Native, Swift, Kotlin",
        "growth": "Medium",
        "salary": "$70,000 - $105,000"
    },
    {
        "id": 7,
        "title": "DevOps Engineer",
        "description": "Automate CI/CD pipelines, monitor deployments, and improve system reliability.",
        "skills": "Linux, Docker, Kubernetes, Jenkins, Git",
        "growth": "High",
        "salary": "$95,000 - $120,000"
    },
    {
        "id": 8,
        "title": "UI/UX Designer",
        "description": "Design intuitive and visually appealing user interfaces and experiences.",
        "skills": "Figma, Adobe XD, Wireframing, Prototyping",
        "growth": "Medium",
        "salary": "$65,000 - $85,000"
    },
    {
        "id": 9,
        "title": "Blockchain Developer",
        "description": "Build decentralized applications (dApps), smart contracts, and blockchain platforms.",
        "skills": "Solidity, Ethereum, Web3.js, Cryptography",
        "growth": "High",
        "salary": "$100,000 - $150,000"
    },
    {
        "id": 10,
        "title": "Product Manager",
        "description": "Oversee product lifecycle, gather requirements, and coordinate development teams.",
        "skills": "Agile, Scrum, Business Strategy, Analytics",
        "growth": "Medium",
        "salary": "$90,000 - $125,000"
    },
    {
        "id": 11,
        "title": "Game Developer",
        "description": "Design and develop engaging games for PC, mobile, or consoles.",
        "skills": "Unity, Unreal Engine, C#, C++",
        "growth": "Medium",
        "salary": "$70,000 - $100,000"
    },
    {
        "id": 12,
        "title": "AI Research Scientist",
        "description": "Conduct advanced AI and machine learning research to develop new algorithms and models.",
        "skills": "Mathematics, Deep Learning, Reinforcement Learning, Python",
        "growth": "High",
        "salary": "$110,000 - $160,000"
    }
]

# Utility: parse salary strings into numbers
def parse_salary(salary_str):
    parts = salary_str.replace("$", "").replace(",", "").split("-")
    if len(parts) == 2:
        return int(parts[0].strip()), int(parts[1].strip())
    return None, None


# Show career suggestions (with filters + sorting)
@career_bp.route("/suggestions")
def career_suggestions():
    keyword = request.args.get("keyword", "").lower()
    demand_filter = request.args.get("demand", "")
    salary_filter = request.args.get("salary", "")
    sort_order = request.args.get("sort", "")

    filtered = career_list

    # Keyword search
    if keyword:
        filtered = [
            c for c in filtered
            if keyword in c["title"].lower()
            or keyword in c["skills"].lower()
            or keyword in c["description"].lower()
        ]

    # Demand filter
    if demand_filter:
        filtered = [c for c in filtered if c["growth"].lower() == demand_filter.lower()]

    # Salary filter
    if salary_filter:
        if salary_filter == "low":  # Below $80k
            filtered = [c for c in filtered if parse_salary(c["salary"])[1] <= 80000]
        elif salary_filter == "mid":  # $80k–$110k
            filtered = [c for c in filtered if 80000 <= parse_salary(c["salary"])[0] <= 110000]
        elif salary_filter == "high":  # Above $110k
            filtered = [c for c in filtered if parse_salary(c["salary"])[0] >= 110000]

    # Sorting by salary
    if sort_order == "asc":
        filtered.sort(key=lambda c: parse_salary(c["salary"])[0])
    elif sort_order == "desc":
        filtered.sort(key=lambda c: parse_salary(c["salary"])[1], reverse=True)

    return render_template("career_suggestions.html", careers=filtered)


# Save a career (by ID instead of title)
@career_bp.route("/save/<int:career_id>")
def save_career(career_id):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    # Example: get career details by ID from your DB or list
    # For now, assume you pass `careers` to the template and find the one
    career = next((c for c in CAREERS if c["id"] == career_id), None)

    if career:
        save_career_db(
            session["user_id"],
            career["title"],
            career.get("description", ""),
            ", ".join(career.get("skills", [])),
            career.get("growth", ""),
            career.get("salary", "")
        )

    return redirect(url_for("career.saved_careers"))



# View saved careers
@career_bp.route("/saved")
def saved_careers():
    if "user" not in session:
        return redirect(url_for("auth.login"))

    user = get_user_by_username(session["user"])
    careers = get_saved_careers(user[0])
    return render_template("saved_careers.html", careers=careers)


# Remove a saved career (still by DB id)
@career_bp.route("/remove/<int:career_id>")
def remove_career(career_id):
    if "user" not in session:
        return redirect(url_for("auth.login"))

    user = get_user_by_username(session["user"])
    remove_saved_career(career_id, user[0])
    flash("Career removed successfully!", "info")
    return redirect(url_for("career.saved_careers"))
