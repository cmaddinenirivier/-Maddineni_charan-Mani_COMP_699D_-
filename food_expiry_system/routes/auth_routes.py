from flask import Blueprint, render_template, request, redirect, session
from models.user import create_user, validate_user, get_user_by_email

auth_bp = Blueprint('auth', __name__)


def is_logged_in():
    return 'user_id' in session


@auth_bp.route('/', methods=['GET', 'POST'])
def login():
    if is_logged_in():
        return redirect('/dashboard')

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = validate_user(email, password)

        if user:
            session['user_id'] = user['id']
            return redirect('/dashboard')
        else:
            return render_template('login.html', error="Invalid email or password")

    return render_template('login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if is_logged_in():
        return redirect('/dashboard')

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        if not name or not email or not password:
            return render_template('register.html', error="All fields are required")

        existing_user = get_user_by_email(email)

        if existing_user:
            return render_template('register.html', error="Email already exists")

        success = create_user(name, email, password)

        if success:
            return redirect('/')
        else:
            return render_template('register.html', error="Registration failed")

    return render_template('register.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')