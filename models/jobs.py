# models/jobs.py

jobs_by_company = {
    "Google": [
        {"title": "Software Engineer", "location": "Bangalore, India", "url": "https://careers.google.com/jobs/results/"},
        {"title": "Data Scientist", "location": "Hyderabad, India", "url": "https://careers.google.com/jobs/results/"},
        {"title": "Cloud Engineer", "location": "Remote", "url": "https://careers.google.com/jobs/results/"},
    ],
    "Microsoft": [
        {"title": "Software Developer", "location": "Hyderabad, India", "url": "https://careers.microsoft.com/"},
        {"title": "AI Engineer", "location": "Bangalore, India", "url": "https://careers.microsoft.com/"},
        {"title": "Security Analyst", "location": "Noida, India", "url": "https://careers.microsoft.com/"},
    ],
    "Amazon": [
        {"title": "SDE I", "location": "Hyderabad, India", "url": "https://www.amazon.jobs/"},
        {"title": "Solutions Architect", "location": "Bangalore, India", "url": "https://www.amazon.jobs/"},
        {"title": "Product Manager", "location": "Chennai, India", "url": "https://www.amazon.jobs/"},
    ],
    "Meta": [
        {"title": "Backend Engineer", "location": "London, UK", "url": "https://www.metacareers.com/jobs"},
        {"title": "Machine Learning Engineer", "location": "Remote", "url": "https://www.metacareers.com/jobs"},
    ],
    "Apple": [
        {"title": "iOS Engineer", "location": "California, USA", "url": "https://jobs.apple.com/"},
        {"title": "Hardware Engineer", "location": "Bangalore, India", "url": "https://jobs.apple.com/"},
    ],
    "Netflix": [
        {"title": "Data Engineer", "location": "California, USA", "url": "https://jobs.netflix.com/"},
        {"title": "Machine Learning Scientist", "location": "Remote", "url": "https://jobs.netflix.com/"},
    ],
    "Adobe": [
        {"title": "DevOps Engineer", "location": "Mumbai, India", "url": "https://adobe.wd5.myworkdayjobs.com/en-US/external_experienced"},
        {"title": "Cloud Engineer", "location": "Noida, India", "url": "https://adobe.wd5.myworkdayjobs.com/en-US/external_experienced"},
    ],
    "Infosys": [
        {"title": "Software Engineer", "location": "Pune, India", "url": "https://career.infosys.com/"},
        {"title": "Java Developer", "location": "Hyderabad, India", "url": "https://career.infosys.com/"},
    ],
    "TCS": [
        {"title": "Frontend Developer", "location": "Chennai, India", "url": "https://www.tcs.com/careers"},
        {"title": "Data Analyst", "location": "Bangalore, India", "url": "https://www.tcs.com/careers"},
    ],
    "Wipro": [
        {"title": "Cloud Architect", "location": "Pune, India", "url": "https://careers.wipro.com/"},
        {"title": "System Engineer", "location": "Noida, India", "url": "https://careers.wipro.com/"},
    ],
    "Accenture": [
        {"title": "Consultant", "location": "Bangalore, India", "url": "https://www.accenture.com/in-en/careers"},
        {"title": "AI Analyst", "location": "Hyderabad, India", "url": "https://www.accenture.com/in-en/careers"},
    ],
}

# ✅ Add 80+ auto-generated placeholder jobs (so we reach 100+ total)
companies = ["Google", "Microsoft", "Amazon", "Meta", "Apple", "Netflix",
             "Adobe", "Infosys", "TCS", "Wipro", "Accenture"]

roles = [
    "Software Engineer", "Data Scientist", "AI Engineer", "DevOps Engineer",
    "Frontend Developer", "Backend Developer", "Full Stack Developer",
    "Cloud Architect", "System Engineer", "Data Analyst"
]

locations = ["Bangalore, India", "Hyderabad, India", "Pune, India",
             "Chennai, India", "Noida, India", "Remote"]

# Auto-generate jobs and add to jobs_by_company
import random

for _ in range(80):  # generate 80 extra jobs
    company = random.choice(companies)
    role = random.choice(roles)
    location = random.choice(locations)
    # For auto-generated jobs, still point to company’s official career site
    url_map = {
        "Google": "https://careers.google.com/jobs/results/",
        "Microsoft": "https://careers.microsoft.com/",
        "Amazon": "https://www.amazon.jobs/",
        "Meta": "https://www.metacareers.com/jobs",
        "Apple": "https://jobs.apple.com/",
        "Netflix": "https://jobs.netflix.com/",
        "Adobe": "https://adobe.wd5.myworkdayjobs.com/en-US/external_experienced",
        "Infosys": "https://career.infosys.com/",
        "TCS": "https://www.tcs.com/careers",
        "Wipro": "https://careers.wipro.com/",
        "Accenture": "https://www.accenture.com/in-en/careers",
    }
    url = url_map[company]
    jobs_by_company[company].append({
        "title": role,
        "location": location,
        "url": url
    })
