from flask import Blueprint, render_template, request
from models.interview_questions import interview_questions

interview_bp = Blueprint("interview", __name__, template_folder="../templates")

@interview_bp.route("/interview-prep")
def interview_prep():
    company_filter = request.args.get("company", "").strip()
    keyword = request.args.get("keyword", "").strip().lower()

    filtered_questions = {}

    for company, questions in interview_questions.items():
        # Apply company filter
        if company_filter and company.lower() != company_filter.lower():
            continue

        # Apply keyword filter
        if keyword:
            matched = [q for q in questions if keyword in q.lower()]
            if matched:
                filtered_questions[company] = matched
        else:
            filtered_questions[company] = questions

    return render_template(
        "interview.html",
        interview_questions=filtered_questions,
        company_filter=company_filter,
        keyword=keyword,
        companies=list(interview_questions.keys())
    )
