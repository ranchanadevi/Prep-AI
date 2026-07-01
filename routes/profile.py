from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db
from models.user import User
from models.quiz_scores import QuizScore
from models.mock_interviews import MockInterview
from routes.auth import login_required, is_strong_password

profile_bp = Blueprint('profile', __name__, url_prefix='/profile')

@profile_bp.route('/')
@login_required
def index():
    user_id = session['user_id']
    user = User.query.get(user_id)
    if not user:
        return redirect(url_for('auth.login'))

    # Fetch full score histories
    quizzes = QuizScore.query.filter_by(user_id=user_id).order_by(QuizScore.created_at.desc()).all()
    
    # Fetch full mock interview histories
    mocks = MockInterview.query.filter_by(user_id=user_id).order_by(MockInterview.created_at.desc()).all()

    return render_template(
        'profile.html',
        user=user,
        quizzes=quizzes,
        mocks=mocks
    )

@profile_bp.route('/update', methods=['POST'])
@login_required
def update():
    user_id = session['user_id']
    user = User.query.get(user_id)
    if not user:
        return redirect(url_for('auth.login'))

    full_name = request.form.get('full_name', '').strip()
    college_name = request.form.get('college_name', '').strip()
    department = request.form.get('department', '').strip()
    year_of_study = request.form.get('year_of_study', '')

    if not (full_name and college_name and department and year_of_study):
        flash("All fields are required to update profile details.", "error")
        return redirect(url_for('profile.index'))

    try:
        year_of_study = int(year_of_study)
        if year_of_study < 1 or year_of_study > 5:
            raise ValueError
    except ValueError:
        flash("Please select a valid year of study.", "error")
        return redirect(url_for('profile.index'))

    # Save changes
    user.full_name = full_name
    user.college_name = college_name
    user.department = department
    user.year_of_study = year_of_study

    try:
        db.session.commit()
        session['user_name'] = full_name  # Update display name
        flash("Profile updated successfully!", "success")
    except Exception as e:
        db.session.rollback()
        print(f"Error updating user profile: {e}")
        flash("Failed to update profile details in database.", "error")

    return redirect(url_for('profile.index'))

@profile_bp.route('/change-password', methods=['POST'])
@login_required
def change_password():
    user_id = session['user_id']
    user = User.query.get(user_id)
    if not user:
        return redirect(url_for('auth.login'))

    current_pass = request.form.get('current_password', '')
    new_pass = request.form.get('new_password', '')
    confirm_new = request.form.get('confirm_new_password', '')

    if not (current_pass and new_pass and confirm_new):
        flash("All fields are required to change password.", "error")
        return redirect(url_for('profile.index'))

    # Verify current password
    if not user.check_password(current_pass):
        flash("Incorrect current password.", "error")
        return redirect(url_for('profile.index'))

    # Validate new password
    if not is_strong_password(new_pass):
        flash("New password must be at least 8 characters long and contain both letters and numbers.", "error")
        return redirect(url_for('profile.index'))

    if new_pass != confirm_new:
        flash("New passwords do not match.", "error")
        return redirect(url_for('profile.index'))

    # Set new password
    user.set_password(new_pass)
    
    try:
        db.session.commit()
        flash("Password updated successfully!", "success")
    except Exception as e:
        db.session.rollback()
        print(f"Error modifying password: {e}")
        flash("Failed to save new password. Please try again.", "error")

    return redirect(url_for('profile.index'))
