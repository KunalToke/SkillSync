from flask import Blueprint, render_template, session, redirect, url_for, request
from models.resources import resources

skills_bp = Blueprint('skills', __name__, template_folder='../templates')

@skills_bp.route('/skills')
def skills():
    if "user" not in session:
        return redirect(url_for('auth.login'))

    # Get filters from query params
    category_filter = request.args.get("category", "").lower()
    search_query = request.args.get("search", "").lower()

    filtered = resources

    # Apply category filter
    if category_filter:
        filtered = [r for r in filtered if r["category"].lower() == category_filter]

    # Apply search filter
    if search_query:
        filtered = [r for r in filtered if search_query in r["title"].lower() or search_query in r["category"].lower()]

    # Get unique categories
    categories = sorted(set(r["category"] for r in resources))

    return render_template(
        "skills.html",
        resources=filtered,
        categories=categories,
        selected_category=category_filter,
        search_query=search_query
    )
