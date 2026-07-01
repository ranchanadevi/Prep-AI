import re
import uuid
from datetime import datetime, timedelta
from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db
from models.user import User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Mock cache to store password reset tokens: {token: (email, expiry_datetime)}
reset_tokens = {}

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please log in to access this page.", "error")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def is_valid_email(email):
    # Basic email pattern
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def is_strong_password(password):
    # Minimum 8 characters, at least one letter and one number
    if len(password) < 8:
        return False
    if not any(char.isdigit() for char in password):
        return False
    if not any(char.isalpha() for char in password):
        return False
    return True

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('dashboard.index'))
        
    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        college_name = request.form.get('college_name', '').strip()
        department = request.form.get('department', '').strip()
        year_of_study = request.form.get('year_of_study', '')

        # Validations
        if not (full_name and email and password and confirm_password and college_name and department and year_of_study):
            flash("All fields are required.", "error")
            return render_template('auth/register.html')

        if not is_valid_email(email):
            flash("Please enter a valid email address.", "error")
            return render_template('auth/register.html')

        if not is_strong_password(password):
            flash("Password must be at least 8 characters long and contain both letters and numbers.", "error")
            return render_template('auth/register.html')

        if password != confirm_password:
            flash("Passwords do not match.", "error")
            return render_template('auth/register.html')

        try:
            year_of_study = int(year_of_study)
            if year_of_study < 1 or year_of_study > 5:
                raise ValueError
        except ValueError:
            flash("Please enter a valid year of study (1-5).", "error")
            return render_template('auth/register.html')

        # Check existing email
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email address already registered.", "error")
            return render_template('auth/register.html')

        # Create user
        new_user = User(
            full_name=full_name,
            email=email,
            college_name=college_name,
            department=department,
            year_of_study=year_of_study
        )
        new_user.set_password(password)

        try:
            db.session.add(new_user)
            db.session.commit()
            flash("Registration successful! Please login.", "success")
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            print(f"Error registering user: {e}")
            flash("A database error occurred. Please try again.", "error")

    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        if not (email and password):
            flash("Please enter both email and password.", "error")
            return render_template('auth/login.html')

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            session.clear()
            session['user_id'] = user.id
            session['user_name'] = user.full_name
            flash(f"Welcome back, {user.full_name}!", "success")
            return redirect(url_for('dashboard.index'))
        else:
            flash("Invalid email or password.", "error")

    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out successfully.", "success")
    return redirect(url_for('landing'))

@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        if not email:
            flash("Please enter your email address.", "error")
            return render_template('auth/forgot_password.html')

        user = User.query.filter_by(email=email).first()
        if user:
            # Generate UUID token expiring in 15 minutes
            token = str(uuid.uuid4())
            expiry = datetime.utcnow() + timedelta(minutes=15)
            reset_tokens[token] = (email, expiry)
            
            # Print to stdout console for developers/testing
            reset_link = url_for('auth.reset_password', token=token, _external=True)
            print(f"--- PASSWORD RESET SIMULATION FOR {email} ---")
            print(f"Token: {token}")
            print(f"Link: {reset_link}")
            print("---------------------------------------------")
            
            # Flash success message with the simulated link so users can test it easily!
            flash(f"Password reset link generated! For local testing, click this link to reset password: {reset_link}", "success")
        else:
            # Prevent user enumeration, but since this is local development let's notify
            flash("If that email is registered, we have simulated a password reset link for you in terminal log.", "success")

    return render_template('auth/forgot_password.html')

@auth_bp.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    token = request.args.get('token') or request.form.get('token')
    if not token or token not in reset_tokens:
        flash("Invalid or missing password reset token.", "error")
        return redirect(url_for('auth.login'))

    email, expiry = reset_tokens[token]
    
    # Check expiry
    if datetime.utcnow() > expiry:
        del reset_tokens[token]
        flash("The password reset token has expired.", "error")
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        if not (password and confirm_password):
            flash("Both fields are required.", "error")
            return render_template('auth/reset_password.html', token=token)

        if not is_strong_password(password):
            flash("Password must be at least 8 characters long and contain both letters and numbers.", "error")
            return render_template('auth/reset_password.html', token=token)

        if password != confirm_password:
            flash("Passwords do not match.", "error")
            return render_template('auth/reset_password.html', token=token)

        user = User.query.filter_by(email=email).first()
        if user:
            user.set_password(password)
            try:
                db.session.commit()
                # Remove token
                del reset_tokens[token]
                flash("Your password has been reset successfully! Please log in.", "success")
                return redirect(url_for('auth.login'))
            except Exception as e:
                db.session.rollback()
                print(f"Error resetting password: {e}")
                flash("Could not update password. Please try again.", "error")
        else:
            flash("User not found.", "error")

    return render_template('auth/reset_password.html', token=token)
