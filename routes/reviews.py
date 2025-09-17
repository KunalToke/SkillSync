from flask import Blueprint, render_template, session, redirect, url_for, request

reviews_bp = Blueprint('reviews', __name__, template_folder='../templates')

reviews = []

@reviews_bp.route('/reviews', methods=['GET', 'POST'])
def reviews_page():
    if "user" not in session:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        reviewer = session['user']
        reviewed_user = request.form.get('reviewed_user')
        rating = request.form.get('rating')
        comment = request.form.get('comment')
        reviews.append({
            'reviewer': reviewer,
            'reviewed_user': reviewed_user,
            'rating': rating,
            'comment': comment
        })

    return render_template('reviews.html', reviews=reviews)
