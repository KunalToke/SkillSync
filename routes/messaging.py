from flask import Blueprint, render_template, session, redirect, url_for, request

messaging_bp = Blueprint('messaging', __name__, template_folder='../templates')

messages = []

@messaging_bp.route('/messages', methods=['GET', 'POST'])
def messages_page():
    if "user" not in session:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        sender = session['user']
        recipient = request.form.get('recipient')
        content = request.form.get('content')
        messages.append({'sender': sender, 'recipient': recipient, 'content': content})

    return render_template('messages.html', messages=messages)
